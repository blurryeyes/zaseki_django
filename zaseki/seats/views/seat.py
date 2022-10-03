from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render, get_object_or_404
from django.utils import timezone

import logging

from seats.models import Layout, Seat, Usage

logger = logging.getLogger('django')


@login_required
def seat_list(request):
    seats = Seat.objects.select_related('layout').order_by('id').all()
    layout_name = request.GET.get('layout_name')
    if layout_name is not None:
        seats = seats.filter(layout__layout_name__contains=layout_name)
    return render(request, 'seats/seat_list.html', {'seats' : seats})
