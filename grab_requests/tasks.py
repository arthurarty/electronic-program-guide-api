import subprocess
from typing import Optional

from utils.xml_utils import create_config_xml
from celery import shared_task


@shared_task()
def run_web_grab(
    site: str, site_id: str, xmltv_id: str, site_name: Optional[str] = None
):
    create_config_xml(site, site_id, xmltv_id, site_name)
    # Define the path to your bash script
    script_path = '.wg++/run.sh'

    # Start the bash script using subprocess
    process = subprocess.Popen(
        ['bash', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Wait for the script to finish and capture the output
    stdout, stderr = process.communicate()

    # Print the output
    print("Standard Output:\n", stdout.decode())
    print("Standard Error:\n", stderr.decode())
