from grab_requests.models import GrabRequest
from rest_framework import serializers
from typing import Dict, Any


class GrabRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrabRequest
        fields = ['id', 'site', 'site_id', 'xmltv_id', 'result_xml']
        read_only_fields = ['result_xml', 'id']
