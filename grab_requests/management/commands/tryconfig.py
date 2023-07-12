from xml.sax.saxutils import escape

from django.core.management.base import BaseCommand

from utils.xml_utils import create_config_xml


class Command(BaseCommand):
    help = "Create a test config file"

    def handle(self, *args, **options):
        channel_name="Cambridgeshire & Bedfordshire - Paramount Network"
        guide_file_name = channel_name.strip().replace(' ', '').replace('(', '').replace(')', '')
        guide_file_name = escape(guide_file_name)
        guide_file_name = f'{guide_file_name}_guide.xml'
        print(guide_file_name)
        create_config_xml(
            site="tv.bt.com.E",
            site_id="hsvx",
            xmltv_id="Cambridgeshire & Bedfordshire - Paramount Network",
            channel_name=channel_name,
            guide_name=guide_file_name,
            file_path='.wg++/WebGrab++.test_config.xml'
        )
    