from utils.xml_utils import create_config_xml
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a test config file"

    def handle(self, *args, **options):
        channel_name="TV 100 HD (37)"
        guide_file_name = channel_name.strip().replace(' ', '').replace('(', '').replace(')', '')
        guide_file_name = f'{guide_file_name}_guide.xml'
        create_config_xml(
            site="digiturk.com.tr",
            site_id="527##72x44_tv100.png",
            xmltv_id="TV 100 HD (37)",
            channel_name=channel_name,
            guide_name=guide_file_name,
            file_path='.wg++/WebGrab++.test_config.xml'
        )
