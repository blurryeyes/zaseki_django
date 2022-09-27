from django.urls import path
from django.views.generic import CreateView

from seats import views, admin

urlpatterns = [
    path('', views.top, name='top'),
    path('layout/', views.layout_list, name='layout_list'),
    path('layout/new/', views.layout_new, name='layout_new'),
    path('layout/<int:layout_id>/', views.layout_detail, name='layout_detail'),
    path('layout/<int:layout_id>/edit/', views.layout_edit, name='layout_edit'),
    path('layout/<int:layout_id>/delete/', views.layout_delete, name='layout_delete'),
    path('seat/', views.seat_list, name='seat_list'),
    path('seat/place/<int:layout_id>/', views.seat_place, name='seat_place'),
    path('seat/sit/<int:layout_id>/', views.seat_sit, name='seat_sit'),
    path('seat/view/<int:layout_id>/', views.seat_view, name='seat_view'),
    path('usage/', views.usage_list, name='usage_list'),
    path('usagelog/', views.usagelog_list, name='usagelog_list'),
]
