from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import logging

from seats.models import Usage

logger = logging.getLogger('django')


@login_required
def usage_list(request):
    usages = Usage.objects.prefetch_related('user').order_by('id').all()
    last_name = request.GET.get('last_name')
    if last_name is not None:
        usages = usages.filter(user__last_name__contains=last_name)
    first_name = request.GET.get('first_name')
    if first_name is not None:
        usages = usages.filter(user__first_name__contains=first_name)
    return render(request, 'seats/usage_list.html', {'usages' : usages})
