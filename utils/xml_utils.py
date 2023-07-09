"""
Functions we are going to use to create and read the xml files
"""
import os
import xml.etree.ElementTree as ET
from typing import Optional

from common.custom_logging import logger
from utils.settings import get_setting

DEFAULT_XML_STR = """<?xml version="1.0"?>
<settings>
  <filename>{guide_name}</filename>
  <mode></mode>
  <postprocess grab="y" run="n">rex</postprocess>
  <user-agent>Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71</user-agent>
  <logging>on</logging>
  <retry time-out="5">{retry}</retry>
  <timespan>{time_span}</timespan>
  <update>f</update>
  <channel site="{site}" site_id="{site_id}" xmltv_id="{xmltv_id}">{site_name}</channel>
  {additional_tags}
</settings>
"""


def prepare_offset_tag(offset: str, xmltv_id: str, site_name: str, suffix_int: int) -> str:
    return f'<channel offset="{offset}" same_as="{xmltv_id}" xmltv_id="{xmltv_id}_{suffix_int}">{site_name}</channel>'


def create_config_xml(
    site: str,
    site_id: str,
    xmltv_id: str,
    guide_name: str,
    channel_name: Optional[str] = None,
    offset: Optional[str] = None,
    file_path: Optional[str] = '.wg++/WebGrab++.config.xml',
):
    """
    Creates an xml config file for channel to run web_grub against.
    """
    if not channel_name:
        channel_name = xmltv_id
    timespan = get_setting('timespan')
    retry = get_setting('retry')
    wg_username = get_setting('WG_USERNAME')
    wg_email = get_setting('WG_EMAIL')
    wg_password = get_setting('WG_PASSWORD')

    try:
        timespan = int(timespan) if timespan else 0
        retry = int(retry) if retry else 4
    except ValueError as exception:
        logger.info('Incorrect value for setting of timespan or retry. Expected integers')
        logger.info('Failed to create config xml')
        raise exception
    logger.info('Using settings -> Timespan: %s, retry: %s', timespan, retry)
    additional_tags = ''
    if offset:
        additional_tags += prepare_offset_tag(offset, xmltv_id, channel_name, 2)
    if wg_username and wg_email and wg_password:
        logger.info('Using the web grab license')
        wg_license = f'<license wg-username="{wg_username}" registered-email="{wg_email}" password="{wg_password}" />'
        additional_tags += wg_license
    xml_str = DEFAULT_XML_STR.format(
        site=site,
        site_id=site_id,
        xmltv_id=xmltv_id,
        site_name=channel_name,
        time_span=timespan,
        retry=retry,
        additional_tags=additional_tags,
        guide_name=guide_name,
    )
    root = ET.fromstring(xml_str)
    print(xml_str)
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    logger.info('Done writing config xml file')


def delete_file(file_path: str) -> bool:
    try:
        os.remove(file_path)
        logger.info("File '%s' deleted successfully.", file_path)
        return True
    except OSError as raised_error:
        logger.info("Error occurred while deleting file '%s': %s", file_path, raised_error)
        return False
