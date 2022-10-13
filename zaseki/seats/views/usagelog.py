from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

import logging

from seats.models import UsageLog
from zaseki.myutils import str_to_timezone

logger = logging.getLogger('django')


@login_required
def usagelog_list(request):
    usagelogs = UsageLog.objects.select_related('layout').select_related('seat').select_related('user').order_by('id').all()
    layout_name = request.GET.get('layout_name')
    if layout_name:
        usagelogs = usagelogs.filter(layout__layout_name__contains=layout_name)
    last_name = request.GET.get('last_name')
    if last_name:
        usagelogs = usagelogs.filter(user__last_name__contains=last_name)
    first_name = request.GET.get('first_name')
    if first_name:
        usagelogs = usagelogs.filter(user__first_name__contains=first_name)
    sitting_time_begin = str_to_timezone(request.GET.get('sitting_time_begin'))
    if sitting_time_begin is not None:
        usagelogs = usagelogs.filter(Q(sit_datetime__gte=sitting_time_begin) | ~Q(leave_datetime__lte=sitting_time_begin))
    sitting_time_end = str_to_timezone(request.GET.get('sitting_time_end'))
    if sitting_time_end is not None:
        usagelogs = usagelogs.filter(Q(sit_datetime__lte=sitting_time_end) | ~Q(leave_datetime__gte=sitting_time_end))
    params = {
        'usagelogs' : usagelogs,
        }
    return render(request, 'seats/usagelog_list.html', params)

