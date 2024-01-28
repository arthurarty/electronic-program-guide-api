import xml.etree.ElementTree as ET
from urllib.parse import urlparse

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import generics, status
from rest_framework.parsers import FileUploadParser
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from common.custom_logging import logger
from grab_requests.models import GrabRequest, GrabSetting
from grab_requests.serializers import (ExternalTvGuideSerializer,
                                       FileNameSerializer,
                                       GrabRequestSerializer,
                                       GrabSettingSerializer, GrabSettingUpdateSerializer)
from utils.files import (delete_file_if_exists, download_file,
                         list_files_in_directory)
from utils.update_site_pack import clone_git_repo
from utils.xml_utils import parse_xml_file, delete_file
from utils.settings import get_setting
from grab_requests.tasks import send_xml_guide


class GrabRequestListView(generics.ListCreateAPIView):
    queryset = GrabRequest.objects.order_by('-created_at').all()[:60]
    serializer_class = GrabRequestSerializer


class GrabRequestDetailView(generics.RetrieveAPIView):
    queryset = GrabRequest.objects.all()
    serializer_class = GrabRequestSerializer


class GrabRequestBulkCreateView(APIView):
    def post(self, request: HttpRequest, format=None)-> Response:
        serializer = GrabRequestSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GrabSettingListView(generics.ListCreateAPIView):
    queryset = GrabSetting.objects.order_by('-created_at').all()[:60]
    serializer_class = GrabSettingSerializer


class GrabSettingDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = GrabSettingSerializer
    queryset = GrabSetting.objects.all()


class GrabSettingUpdateView(APIView):
    serializer_class = GrabSettingUpdateSerializer

    def put(self, request: HttpRequest, format=None) -> Response:
        serializer = GrabSettingUpdateSerializer(data=request.data, many=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        setting_name = serializer.data['setting_name']
        grab_setting = GrabSetting.objects.filter(setting_name=setting_name).first()
        if not grab_setting:
            return Response('No such setting', status=status.HTTP_404_NOT_FOUND)
        setting_value = serializer.data['setting_value']
        grab_setting.setting_value = setting_value
        grab_setting.save()
        updated_serializer = GrabSettingSerializer(grab_setting)
        return Response(updated_serializer.data, status=status.HTTP_200_OK)


class UpdateSitePack(APIView):
    """
    Update the siteini.pack which contains channels by country.
    To do that we pull the webgrabplus repo the copy the siteini.pack
    to the .wg++ folder. 
    """
    def get(self, request: HttpRequest, format=None) -> Response:
        clone_git_repo(
            repo_url='https://github.com/SilentButeo2/webgrabplus-siteinipack.git',
            folder_path=f'{settings.BASE_DIR}/temp',
            root_path=settings.BASE_DIR,
            destination_folder=f'{settings.BASE_DIR}/.wg++/siteini.pack'
        )
        return Response('Request to update received', status=status.HTTP_200_OK)


class FileUploadView(APIView):
    """
    Class to handle uploading of custom .ini files.
    """
    parser_classes = [FileUploadParser]

    def post(self, request: HttpRequest, filename: str, format=None) -> Response:
        accepted_file_paths = ('.ini', '.xml')
        if not filename.endswith(accepted_file_paths):
            logger.info('File uploaded has unacceptable file extension')
            return Response('Invalid file type.', status=status.HTTP_400_BAD_REQUEST)
        file_obj = request.data['file']
        destination_path = f'{settings.BASE_DIR}/.wg++/siteini.user'
        FileSystemStorage(location=destination_path).save(filename, file_obj)
        return Response('Custom ini received.', status=status.HTTP_201_CREATED)


class ListCustomIni(APIView):
    """
    List all files uploaded to the folder 'siteini.user'.
    """
    def get(self, request: HttpRequest):
        """
        Returns a list of the files present.
        """
        directory_path = f'{settings.BASE_DIR}/.wg++/siteini.user'
        file_list = list_files_in_directory(directory_path)
        return Response(
            {
                'files': file_list
            },
            status=status.HTTP_200_OK
        )


class DeleteCustomIni(APIView):
    def post(self, request: HttpRequest) -> Response:
        """
        Handles deleting the file.
        """
        serializer = FileNameSerializer(data=request.data, many=False)
        if serializer.is_valid():
            file_name = serializer.data['file_name']
            file_to_delete = f'{settings.BASE_DIR}/.wg++/siteini.user/{file_name}'
            return delete_file_if_exists(file_to_delete)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExternalTvGuides(APIView):
    """
    Handles downloading external tv guide xml
    parsing it and kicking off tasks to handle it.
    """
    def post(self, request: HttpRequest) -> Response:
        # TODO: This function should be async because it takes at least 30 secs
        serializer = ExternalTvGuideSerializer(data=request.data, many=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        download_url = serializer.data['download_url']
        external_id = serializer.data['external_id']
        parsed_url = urlparse(download_url)
        file_name = parsed_url.path
        file_name = file_name.replace('/', '')
        was_downloaded = download_file(download_url, file_name)
        if was_downloaded:
            xml_root = parse_xml_file(file_name)
            delete_file(file_name)
            return handle_channels_from_xml(xml_root, external_id) if xml_root else Response(
                {'msg': 'Failed to parse channels'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {'msg': 'Failed to download'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def handle_channels_from_xml(root: ET, external_id: str) -> Response:
    """
    Extract channels and program guides from xml
    And start async tasks to be handled by workers.
    """
    timeout_str = get_setting("TIMEOUT")
    timeout = int(timeout_str) if timeout_str else 60
    channels = root.findall('.//channel')
    for channel in channels:
        channel_root = ET.fromstring(
            "<tv generator-info-name=\"none\" generator-info-url=\"none\">\n"+"</tv>"
        )
        channel_name = channel.find('display-name')
        channel_name = channel_name.text
        channel_id = channel.attrib['id']
        channel_root.append(channel)
        predicate = './/programme[@channel="'+channel_id+'"]'
        programmes = root.findall(predicate)
        for programme in programmes:
            channel_root.append(programme)
        xml_contents = ET.tostring(channel_root, encoding='unicode')
        # send_xml_guide will be broadcast to the workers to be handled async
        send_xml_guide.delay(external_id, xml_contents, timeout)
    logger.info('Done Handling external tv guide')
    return Response({'msg': 'Done handling tv guide'}, status=status.HTTP_200_OK)
