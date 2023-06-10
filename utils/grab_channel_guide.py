import subprocess
from typing import Optional

from utils.xml_utils import create_config_xml


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


if __name__ == "__main__":
    # example of an error to handle
    # run_web_grab(
    #     site="aasthatv.com",
    #     site_id="0",
    #     xmltv_id="aastha-india",
    # )
    run_web_grab(
        site="turksatkablo.com.tr",
        site_id="1",
        xmltv_id="KABLO INFO",
    )

# TODO: Store the result of the log.


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_grab.settings')
# export DJANGO_SETTINGS_MODULE=web_grab.settings
