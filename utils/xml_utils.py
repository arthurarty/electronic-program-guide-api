"""
Functions we are going to use to create and read the xml files
"""
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from typing import Optional

from common.custom_logging import logger
from utils.settings import get_setting
from xml.sax.saxutils import escape
import gzip


DEFAULT_XML_STR = """<?xml version="1.0"?>
<settings>
  <filename>{guide_name}</filename>
  <mode></mode>
  <postprocess grab="y" run="n">rex</postprocess>
  <user-agent>Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71</user-agent>
  <logging>on</logging>
  {retry}
  <timespan>{time_span}</timespan>
  <update>f</update>
  <channel site="{site}" site_id="{site_id}" xmltv_id="{xmltv_id}">{site_name}</channel>
  {additional_tags}
</settings>
"""


def create_file_name(input_str: str) -> str:
    """
    We remove all special characters when naming the file
    """
    file_name = ''.join(single_character for single_character in input_str if single_character.isalnum())
    file_name = file_name.strip()
    return file_name


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
    site=escape(site) if site else None
    site_id=escape(site_id) if site_id else None
    xmltv_id=escape(xmltv_id) if xmltv_id else None
    channel_name=escape(channel_name) if channel_name else None
    timespan = get_setting('timespan')
    retry = get_setting('retry')
    wg_username = get_setting('WG_USERNAME')
    wg_email = get_setting('WG_EMAIL')
    wg_password = get_setting('WG_PASSWORD')
    try:
        timespan = int(timespan) if timespan else 0
        retry = retry if retry.replace("\\", "") else '<retry time-out="5">3</retry>'
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
    else:
        logger.info('Web Grab license is not set.')
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
    tree = ET.ElementTree(root)
    logger.info('Writing config file %s', file_path)
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


def parse_xml_file(file_name: str) -> Optional[Element]:
    """
    Read all the channels in an xml dump and return the root.
    """
    try:
        if file_name.endswith('.xml'):
            with open(file_name, 'r', encoding='utf-8') as file:
                return ET.fromstring(file.read())
        elif file_name.endswith('.gz'):
            with gzip.open(file_name, 'rb') as gz_file:
                xml_content = gz_file.read()
            root = ET.fromstring(xml_content.decode('utf-8'))
            return root
    except Exception as exception_raised:
        logger.info("Failed to parse file %s due to %s", file_name, exception_raised)
        return None
