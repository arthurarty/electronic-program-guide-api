from django.db import models
from common.models import BaseTimeStampedModel
from enum import Enum

class RequestStatusEnum(str, Enum):
    PENDING = 'PENDING'
    COMPLETE = 'COMPLETE'
    ERROR = 'ERROR'


class GrabRequest(BaseTimeStampedModel, models.Model):
    """
    A grab request is a request to get a programming guide
    from a given site/channel.
    """
    site=models.CharField(max_length=255)
    site_id=models.CharField(max_length=255)
    xmltv_id=models.CharField(max_length=255)
    result_xml=models.TextField(blank=True)
    result_log = models.TextField(blank=True)
    status=models.CharField(
        max_length=50, choices=[(choice, choice.value) for choice in RequestStatusEnum], default="PENDING",
    )
    channel_name=models.CharField(max_length=255, blank=True)  # sometimes site_name might be different from xmltv_id
    external_id=models.BigIntegerField(blank=True, null=True)
    icon_tag=models.TextField(blank=True, null=True)
    offset=models.CharField(max_length=255, blank=True)


class GrabSetting(BaseTimeStampedModel, models.Model):
    """
    Settings for grab requests
    """
    setting_name=models.CharField(max_length=255, unique=True)
    setting_value=models.CharField(max_length=255)
