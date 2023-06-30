
from rest_framework import generics

from grab_requests.models import GrabRequest, GrabSetting
from grab_requests.serializers import GrabRequestSerializer, GrabSettingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import HttpRequest


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
