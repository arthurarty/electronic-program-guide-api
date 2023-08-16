from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from grab_requests.models import GrabRequest


class Command(BaseCommand):
    help = "Delete task requests older than a week"

    def handle(self, *args, **options):
        one_week_ago = timezone.now() - timedelta(days=7)
        GrabRequest.objects.filter(created_at__lt=one_week_ago).delete()
        print('Done cleaning up old tasks')
