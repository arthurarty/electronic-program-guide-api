import os
import subprocess
import xml.etree.ElementTree as ET
from typing import Optional, Tuple
from xml.sax.saxutils import escape

import requests
from celery import shared_task
from dotenv import load_dotenv
from func_timeout import FunctionTimedOut, func_timeout
from rest_framework import serializers

from common.custom_logging import logger
from grab_requests.models import GrabRequest, RequestStatusEnum
from utils.xml_utils import create_config_xml, delete_file, create_file_name


DEFAULT_TIMEOUT = 120


load_dotenv()



class Serializer(serializers.ModelSerializer):
    class Meta:
        model = GrabRequest
        fields = '__all__'


def send_call_back(grab_request: GrabRequest) -> requests.Response:
    """
    Send post request to the defined CALL_BACK_URL containing the results
    of a grab_request.
    """
    call_back_url = os.environ.get('CALL_BACK_URL')
    logger.info('Sending data to call_back_url %s', call_back_url)
    serializer = Serializer(grab_request)
    return requests.post(call_back_url, json=serializer.data, timeout=60)


def get_icon_tag(xml_str: str) -> str:
    logger.info('Trying to get icon tag')
    root = ET.fromstring(xml_str)
    channel_tags = root.findall('.//channel')
    for channel_tag in channel_tags:
        icon_tag = channel_tag.find('icon')
        # checking if icon_tag: returns False much as icon tag is set
        # so instead we check the type as a work around
        if type(icon_tag) == type(channel_tag):
            return ET.tostring(icon_tag)
    return None


@shared_task()
def run_web_grab(
    request_id: int,
    site: str,
    site_id: str,
    xmltv_id: str,
    channel_name: Optional[str] = None,
    offset: Optional[str] = None,
    timeout: Optional[int] = None,
):
    logger.info('First run without offset')
    timeout = timeout if timeout else DEFAULT_TIMEOUT
    grab_request: Optional[GrabRequest] = _run_web_grab(request_id, site, site_id, xmltv_id, channel_name, None, timeout)
    if offset:
        # if offset is set, we need to run the grabber twice. First time to pick icon
        logger.info('Running with offset set.')
        grab_request = _run_web_grab(request_id, site, site_id, xmltv_id, channel_name, offset, timeout)
    resp = send_call_back(grab_request)
    logger.info(resp.status_code)
    logger.info(resp.text)


def run_bash_script() -> Tuple[str, str]:
    """
    Using a bash script to trigger the grab.
    """
    # Suggestion: This can be written simpler using subprocess.run as opposed to subprocess.Popen
    script_path = '.wg++/run.sh'
    process = subprocess.Popen(
        ['bash', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Wait for the script to finish and capture the output
    logger.info('Getting the output of running grabber.')
    stdout, stderr = process.communicate()

    standard_output = stdout.decode()
    standard_error = stderr.decode()
    logger.info("Standard Output:\n %s", standard_output)
    logger.info("Standard Error:\n %s", standard_error)
    return standard_output, standard_error


def _run_web_grab(
    request_id: int,
    site: str,
    site_id: str,
    xmltv_id: str,
    channel_name: Optional[str] = None,
    offset: Optional[str] = None,
    timeout: Optional[int] = DEFAULT_TIMEOUT,
) -> Optional[GrabRequest]:
    logger.info('Creating Config file for request: %s', request_id)
    guide_file_name = create_file_name(channel_name) if channel_name else ''
    guide_file_name = escape(guide_file_name)
    guide_file_name = f'{guide_file_name}_guide.xml'
    logger.info('file name: %s', guide_file_name)
    grab_request = GrabRequest.objects.get(id=request_id)
    if not grab_request:
        logger.info('Grab request with id: %s not found', request_id)
        # TODO: Raise a custom exception here.
        raise ValueError('Grab Request not found')
    logger.info('Pulled grab request from db')
    try:
        create_config_xml(
            site, 
            site_id,
            xmltv_id,
            guide_file_name,
            channel_name,
            offset,
        )

        delete_file(f'.wg++/{guide_file_name}')
        logger.info(
            'Starting webgrab for request: %s: %s, Timeout set to: %s',
            request_id, xmltv_id, timeout
        )

        # running the bash script can hang, so we are using a timeout to exit
        standard_output, standard_error = func_timeout(timeout, run_bash_script)

        logger.info('Updating webgrab request: %s', request_id)
        with open(f'.wg++/{guide_file_name}', 'r') as reader:
            xml_tv_guide = reader.read()
            if len(xml_tv_guide) > 1:
                logger.info('We did not get a tv guide')
            grab_request.result_xml=xml_tv_guide
            grab_request.status = RequestStatusEnum.COMPLETE.value
            grab_request.result_log=f'{str(standard_output)} \n {str(standard_error)}'
            if not offset:
                icon_tag = get_icon_tag(xml_tv_guide)
                if icon_tag:
                    grab_request.icon_tag=icon_tag
                else:
                    logger.info('Icon tag not found')
            grab_request.save()
            return grab_request
    except FileNotFoundError:
        logger.info('Grabber failed to create guide.xml for request: %s: %s', request_id, xmltv_id)
        grab_request.status = RequestStatusEnum.ERROR.value
        grab_request.result_log=f'{str(standard_output)} \n {str(standard_error)}'
        grab_request.save()
        return grab_request
    except FunctionTimedOut:
        logger.info('Grabber timed out')
        grab_request.status = RequestStatusEnum.ERROR.value
        grab_request.result_log='Grabber timed out'
        grab_request.save()
        return grab_request
    finally:
        logger.info('Clean up config and guide')
        delete_file(f'.wg++/{guide_file_name}')
        delete_file('.wg++/WebGrab++.config.xml')
