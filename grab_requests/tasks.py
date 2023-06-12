import subprocess
from typing import Optional

from utils.xml_utils import create_config_xml
from celery import shared_task
from grab_requests.models import GrabRequest, RequestStatusEnum
from common.custom_logging import logger


@shared_task()
def run_web_grab(
    request_id: int,
    site: str,
    site_id: str,
    xmltv_id: str,
    site_name: Optional[str] = None,
):
    logger.info('Creating Config file for request: %s', request_id)
    create_config_xml(
        site, 
        site_id,
        xmltv_id,
        site_name
    )
    # Define the path to your bash script
    script_path = '.wg++/run.sh'

    logger.info('Starting webgrab for request: %s: %s', request_id, xmltv_id)
    process = subprocess.Popen(
        ['bash', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Wait for the script to finish and capture the output
    stdout, stderr = process.communicate()

    # Print the output
    standard_output = stdout.decode()
    standard_error = stderr.decode()
    print("Standard Output:\n", standard_output)
    print("Standard Error:\n", stderr.decode())

    try:
        with open('.wg++/guide.xml', 'r') as reader:
            grab_request = GrabRequest.objects.get(id=request_id)
            logger.info('Updating webgrab request: %s', request_id)
            grab_request.result_xml=reader.read()
            grab_request.status = RequestStatusEnum.COMPLETE.value
            grab_request.result_log=f'{str(standard_output)} \n {str(standard_error)}'
            grab_request.save()
    except FileNotFoundError:
        logger.info('Grabber failed to create guide.xml for request: %s: %s', request_id, xmltv_id)
        grab_request = GrabRequest.objects.get(id=request_id)
        grab_request.status = RequestStatusEnum.ERROR.value
        grab_request.result_log=f'{str(standard_output)} \n {str(standard_error)}'
        grab_request.save()
