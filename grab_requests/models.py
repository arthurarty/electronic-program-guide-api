from django.db import models
from common.models import BaseTimeStampedModel


class GrabRequest(BaseTimeStampedModel, models.Model):
    """
    A grab request is a request to get a programming guide
    from a given site/channel.
    """
    site=models.CharField()
    site_id=models.CharField()
    xmltv_id=models.CharField()
    result_xml=models.TextField(blank=True)
