from grab_requests.models import GrabRequest
from rest_framework import serializers
from typing import Dict, Any


class GrabRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    site = serializers.CharField(required=True, allow_blank=False, max_length=300)
    xmltv_id = serializers.CharField(required=True, allow_blank=False, max_length=300)
    result_xml=serializers.CharField(required=False)

    def create(self, validated_data: Dict[str, Any]):
        return GrabRequest.objects.create(**validated_data)

    def update(self, instance: GrabRequest, validated_data: Dict[str, Any]):
        instance.result_xml = validated_data.get('result_xml', instance.result_xml)
        instance.save()
        return instance
