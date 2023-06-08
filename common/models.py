from django.db import models


class BaseTimeStampedModel(models.Model):
    """
    Adds timestamps for created_at, updated_at and deleted_at
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
