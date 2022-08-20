from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Layout, Seat, Usage

admin.site.register(Layout)
admin.site.register(Seat)
admin.site.register(Usage)