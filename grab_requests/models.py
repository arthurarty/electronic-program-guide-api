from django.db import models
from common.models import BaseTimeStampedModel

REQUEST_STATUS = ['PENDING', 'COMPLETE', 'ERROR']

class GrabRequest(BaseTimeStampedModel, models.Model):
    """
    A grab request is a request to get a programming guide
    from a given site/channel.
    """
    REQUEST_STATUS_CHOICES=models.TextChoices('Request_Status_Choices', " ".join(REQUEST_STATUS))
    site=models.CharField(max_length=255)
    site_id=models.CharField(max_length=255)
    xmltv_id=models.CharField(max_length=255)
    result_xml=models.TextField(blank=True)
    result_log = models.TextField(blank=True)
    status=models.CharField(
        max_length=50, choices=REQUEST_STATUS_CHOICES.choices, default="PENDING",
    )
    site_name=models.CharField(max_length=255, blank=True)  # sometimes site_name might be different from xmltv_id
