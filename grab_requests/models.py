from django.db import models
from common.models import BaseTimeStampedModel


class GrabRequest(BaseTimeStampedModel, models.Model):
    """
    A grab request is a request to get a programming guide
    from a given site/channel.
    """
    site=models.CharField(max_length=255)
    site_id=models.CharField(max_length=255)
    xmltv_id=models.CharField(max_length=255)
    result_xml=models.TextField(blank=True)
