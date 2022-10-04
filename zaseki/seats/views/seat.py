from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import logging

from seats.models import Seat, Usage, UsageLog

logger = logging.getLogger('django')


@login_required
def seat_list(request):
    seats = Seat.objects.select_related('layout').order_by('id').all()
    layout_name = request.GET.get('layout_name')
    if layout_name is not None:
        seats = seats.filter(layout__layout_name__contains=layout_name)
    return render(request, 'seats/seat_list.html', {'seats' : seats})


@login_required
def seat_detail(request, seat_id):
    seat = Seat.objects.select_related('layout').get(id=seat_id)
    usage = Usage.objects.select_related('user').filter(seat = seat_id).first()
    usagelogs = UsageLog.objects.select_related('user').filter(seat = seat_id)
    params = {
        'seat' : seat,
        'usage' : usage,
        'usagelogs' : usagelogs
        }
    return render(request, 'seats/seat_detail.html', params)
