from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import logging

from seats.models import Usage
from zaseki.myutils import str_to_timezone

logger = logging.getLogger('django')


@login_required
def usage_list(request):
    usages = Usage.objects.select_related('user').select_related('seat__layout').order_by('id').all()
    layout_name = request.GET.get('layout_name')
    if layout_name:
        usages = usages.filter(seat__layout__layout_name__contains=layout_name)
    last_name = request.GET.get('last_name')
    if last_name is not None:
        usages = usages.filter(user__last_name__contains=last_name)
    first_name = request.GET.get('first_name')
    if first_name is not None:
        usages = usages.filter(user__first_name__contains=first_name)
    sitting_time_begin = str_to_timezone(request.GET.get('sitting_time_begin'))
    if sitting_time_begin is not None:
        usages = usages.filter(sit_datetime__gte=sitting_time_begin)
    sitting_time_end = str_to_timezone(request.GET.get('sitting_time_end'))
    if sitting_time_end is not None:
        usages = usages.filter(sit_datetime__lte=sitting_time_end)
    params = {
        'usages' : usages,
        }
    return render(request, 'seats/usage_list.html', params)


@login_required
def usage_detail(request, usage_id):
    usage = Usage.objects.select_related('user').select_related('seat__layout').filter(id=usage_id).first()
    params = {
        'usage' : usage,
        }
    return render(request, 'seats/usage_detail.html', params)
