from typing import Any, Dict

from rest_framework import serializers

from grab_requests.models import GrabRequest, GrabSetting
from grab_requests.tasks import run_web_grab
from utils.settings import get_setting


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
            'channel_name',
            'created_at',
            'updated_at',
            'external_id',
            'offset',
            'icon_tag',
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
        timeout_str = get_setting("TIMEOUT")
        timeout = int(timeout_str) if timeout_str else None
        # .delay is how we add a task to the queue using Celery
        run_web_grab.delay(
            grab_request.id,
            grab_request.site,
            grab_request.site_id,
            grab_request.xmltv_id,
            grab_request.channel_name,
            grab_request.offset,
            timeout,
        )
        return grab_request


class GrabSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model=GrabSetting
        fields='__all__'


class FileNameSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=255)
