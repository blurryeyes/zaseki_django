from django.utils import timezone

import datetime
import logging

logger = logging.getLogger('django')


INPUT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M'

def str_to_timezone(str_datetime):
    return timezone.make_aware(datetime.datetime.strptime(str_datetime, INPUT_DATETIME_FORMAT), timezone.get_default_timezone()) if str_datetime else None
