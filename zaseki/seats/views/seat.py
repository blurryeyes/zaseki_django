from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import logging

from seats.models import Layout, Seat, Usage, UsageLog

logger = logging.getLogger('django')


@login_required
def seat_list(request):
    seats = Seat.objects.select_related('layout').order_by('id').all()
    layout_name = request.GET.get('layout_name')
    if layout_name is not None:
        seats = seats.filter(layout__layout_name__contains=layout_name)
    params = {
        'seats' : seats,
        }
    return render(request, 'seats/seat_list.html', params)


@login_required
def seat_detail(request, seat_id):
    seat = Seat.objects.select_related('layout').get(id=seat_id)
    usage = Usage.objects.select_related('user').filter(seat=seat_id).first()
    usagelogs = UsageLog.objects.select_related('user').filter(seat=seat_id).order_by('sit_datetime')
    params = {
        'seat' : seat,
        'usage' : usage,
        'usagelogs' : usagelogs,
        }
    return render(request, 'seats/seat_detail.html', params)


@login_required
def seat_locate(request, seat_id):
    view_type = 'view'
    logger.info("特定する座席を取得します。")
    locate_seat = Seat.objects.get(id=seat_id)
    logger.info("特定する座席を取得しました。")
    logger.info("レイアウトを取得します。")
    layout = Layout.objects.get(id=locate_seat.layout.id)
    logger.info("レイアウトを取得しました。")
    logger.info("座席を取得します。")
    # https://chuna.tech/detail/49/
    seats = Seat.objects.prefetch_related('user').filter(layout=locate_seat.layout.id)
    logger.info("座席を取得しました。")
    params = {
        'view_type': view_type,
        'layout': layout,
        'seats': seats,
        'locate_seat': locate_seat,
        }
    return render(request, 'seats/layout_base.html', params)
