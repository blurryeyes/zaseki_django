from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from seats.views import top

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', top, name='top'),
    path('accounts/', include('accounts.urls')),
    # path('seats/', include('seats.urls')),
    path('', include('seats.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# ]
