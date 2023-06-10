"""
Functions we are going to use to create and read the xml files
"""
from typing import Optional
import xml.etree.ElementTree as ET
from common.custom_logging import logger


DEFAULT_XML_STR = """<?xml version="1.0"?>
<settings>
  <filename>guide.xml</filename>
  <mode></mode>
  <postprocess grab="y" run="n">rex</postprocess>
  <user-agent>Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 Edg/79.0.309.71</user-agent>
  <logging>on</logging>
  <retry time-out="5">4</retry>
  <timespan>0</timespan>
  <update>f</update>
  <channel site="{site}" site_id="{site_id}" xmltv_id="{xmltv_id}">{site_name}</channel>
</settings>
"""


def create_config_xml(
    site: str,
    site_id: str,
    xmltv_id: str,
    site_name: Optional[str] = None,
    file_path: Optional[str] = '.wg++/WebGrab++.config.xml'
):
    """
    Creates an xml config file for channel to run web_grub against.
    """
    if not site_name:
        site_name = xmltv_id
    xml_str = DEFAULT_XML_STR.format(
        site=site,
        site_id=site_id,
        xmltv_id=xmltv_id,
        site_name=site_name
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
