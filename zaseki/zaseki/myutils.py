from django.utils import timezone

import datetime
import logging

logger = logging.getLogger('django')


INPUT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M'

def str_to_timezone(str_datetime):
    return timezone.make_aware(datetime.datetime.strptime(str_datetime, INPUT_DATETIME_FORMAT), timezone.get_default_timezone()) if str_datetime else None

def format_dhms(total_days, total_seconds):
    hms = format_hms(total_seconds)
    d = str(total_days) + '日 ' if total_days != 0 else ''
    formatter = d + hms
    return formatter

def format_hms(total_seconds):
    hours = int(total_seconds / 3600)
    minutes = int((total_seconds % 3600) / 60)
    seconds = int(total_seconds % 60)
    formatter = str(hours).zfill(2) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)
    return formatter
