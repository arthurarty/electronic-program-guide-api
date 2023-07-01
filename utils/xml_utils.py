"""
Functions we are going to use to create and read the xml files
"""
from typing import Optional
import xml.etree.ElementTree as ET
from common.custom_logging import logger
from utils.settings import get_setting


DEFAULT_XML_STR = """<?xml version="1.0"?>
<settings>
  <filename>guide.xml</filename>
  <mode></mode>
  <postprocess grab="y" run="n">rex</postprocess>
  <user-agent>Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71</user-agent>
  <logging>on</logging>
  <retry time-out="5">{retry}</retry>
  <timespan>{time_span}</timespan>
  <update>f</update>
  <channel site="{site}" site_id="{site_id}" xmltv_id="{xmltv_id}">{site_name}</channel>
</settings>
"""


def create_config_xml(
    site: str,
    site_id: str,
    xmltv_id: str,
    channel_name: Optional[str] = None,
    file_path: Optional[str] = '.wg++/WebGrab++.config.xml'
):
    """
    Creates an xml config file for channel to run web_grub against.
    """
    if not channel_name:
        channel_name = xmltv_id
    timespan = get_setting('timespan')
    retry = get_setting('retry')
    try:
        timespan = int(timespan) if timespan else 0
        retry = int(retry) if retry else 4
    except ValueError as exception:
        logger.info('Incorrect value for setting of timespan or retry. Expected integers')
        logger.info('Failed to create config xml')
        raise exception
    logger.info('Using settings -> Timespan: %s, retry: %s', timespan, retry)
    xml_str = DEFAULT_XML_STR.format(
        site=site,
        site_id=site_id,
        xmltv_id=xmltv_id,
        site_name=channel_name,
        time_span=timespan,
        retry=retry,
    )
    root = ET.fromstring(xml_str)
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    logger.info('Done writing config xml file')


if __name__ == "__main__":
    create_config_xml(
        site="turksatkablo.com.tr",
        site_id="1",
        xmltv_id="KABLO INFO",
    )
