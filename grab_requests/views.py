
from rest_framework import generics

from grab_requests.models import GrabRequest
from grab_requests.serializers import GrabRequestSerializer


class GrabRequestListView(generics.ListCreateAPIView):
    queryset = GrabRequest.objects.all()[:60]
    serializer_class = GrabRequestSerializer


class GrabRequestDetailView(generics.RetrieveAPIView):
    queryset = GrabRequest.objects.all()
    serializer_class = GrabRequestSerializer
