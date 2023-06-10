from grab_requests.models import GrabRequest
from rest_framework import serializers
from typing import Dict, Any
from common.custom_logging import logger


class GrabRequestSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data: Dict[str, Any]) -> GrabRequest:
        grab_request = GrabRequest.objects.create(**validated_data)
        logger.info('We are going to do something here. ***********')
        return grab_request
