from grab_requests.models import GrabRequest
from rest_framework import serializers


class GrabRequestSerializer(serializers.ModelSerializer):
    # TODO: Switch this back to a serializers.Serializer so that we can have a custom create
    # custom create function will be the one to handle the web grab
    class Meta:
        model = GrabRequest
        fields = [
            'id',
            'site', 
            'site_id',
            'xmltv_id',
            'result_xml', 
            'status',
            'result_log',
            'site_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'result_xml',
            'id',
            'status',
            'result_log',
            'created_at',
            'updated_at'
        ]
