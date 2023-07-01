import json
import os
import subprocess
from typing import Optional

import requests
from celery import shared_task
from dotenv import load_dotenv
from rest_framework import serializers

from common.custom_logging import logger
from grab_requests.models import GrabRequest, RequestStatusEnum
from utils.xml_utils import create_config_xml

load_dotenv()


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = GrabRequest
        fields = '__all__'


def send_call_back(grab_request: GrabRequest):
    call_back_url = os.environ.get('CALL_BACK_URL')
    logger.info('Sending data to call_back_url %s', call_back_url)
    serializer = Serializer(grab_request)
    return requests.post(call_back_url, data=json.dumps(serializer.data), timeout=60)


@shared_task()
def run_web_grab(
    request_id: int,
    site: str,
    site_id: str,
    xmltv_id: str,
    channel_name: Optional[str] = None,
):
    logger.info('Creating Config file for request: %s', request_id)
    create_config_xml(
        site, 
        site_id,
        xmltv_id,
        channel_name
    )
    script_path = '.wg++/run.sh'

    logger.info('Starting webgrab for request: %s: %s', request_id, xmltv_id)
    process = subprocess.Popen(
        ['bash', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Wait for the script to finish and capture the output
    stdout, stderr = process.communicate()

    standard_output = stdout.decode()
    standard_error = stderr.decode()
    logger.info("Standard Output:\n %s", standard_output)
    logger.info("Standard Error:\n %s", stderr.decode())

    try:
        with open('.wg++/guide.xml', 'r') as reader:
            grab_request = GrabRequest.objects.get(id=request_id)
            logger.info('Updating webgrab request: %s', request_id)
            grab_request.result_xml=reader.read()
            grab_request.status = RequestStatusEnum.COMPLETE.value
            grab_request.result_log=f'{str(standard_output)} \n {str(standard_error)}'
            grab_request.save()
            logger.info('Done Updating now hitting the callback')
            response = send_call_back(grab_request)
            logger.info(response)
    except FileNotFoundError:
        logger.info('Grabber failed to create guide.xml for request: %s: %s', request_id, xmltv_id)
        grab_request = GrabRequest.objects.get(id=request_id)
        grab_request.status = RequestStatusEnum.ERROR.value
        grab_request.result_log=f'{str(standard_output)} \n {str(standard_error)}'
        grab_request.save()
