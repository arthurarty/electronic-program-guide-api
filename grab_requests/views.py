from django.conf import settings
from rest_framework import generics, status
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from grab_requests.models import GrabRequest, GrabSetting
from grab_requests.serializers import (GrabRequestSerializer,
                                       GrabSettingSerializer)
from utils.update_site_pack import clone_git_repo


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
        return Response(status=status.HTTP_200_OK)
