from grab_requests.models import GrabSetting
from typing import Optional


def get_setting(setting_name: str) -> Optional[str]:
    """
    Get the value of a setting from the database
    """
    setting = GrabSetting.objects.filter(setting_name=setting_name).first()
    if setting:
        return setting.setting_value
    return None
