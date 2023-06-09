from grab_requests.models import GrabRequest
from rest_framework import serializers


class GrabRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrabRequest
        fields = ['id', 'site', 'site_id', 'xmltv_id', 'result_xml', 'status', 'result_log', 'site_name']
        read_only_fields = ['result_xml', 'id', 'status', 'result_log']
