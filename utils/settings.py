from grab_requests.models import GrabSetting
from typing import Optional

import os
from dotenv import load_dotenv


load_dotenv()


def get_setting(setting_name: str, check_database: bool = True) -> Optional[str]:
    """
    Get the value of a setting from the database or  .env
    First we check if the setting is set in the .env
    """
    setting = os.environ.get(setting_name)
    if setting:
        return setting
    if not setting and check_database:
        setting = GrabSetting.objects.filter(setting_name=setting_name).first()
        if setting:
            return setting.setting_value
        return None
    return None
