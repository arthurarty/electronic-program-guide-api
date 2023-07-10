from django.core.management.base import BaseCommand
from utils.update_site_pack import clone_git_repo
from django.conf import settings


class Command(BaseCommand):
    help = "Refresh the site.ini pack"

    def handle(self, *args, **options):
        clone_git_repo(
            repo_url='https://github.com/SilentButeo2/webgrabplus-siteinipack.git',
            folder_path=f'{settings.BASE_DIR}/temp',
            root_path=settings.BASE_DIR,
            destination_folder=f'{settings.BASE_DIR}/.wg++/siteini.pack'
        )
