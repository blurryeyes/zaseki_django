from django.urls import path

from seats import views

urlpatterns = [
    # layout
    path('', views.layout.top, name='top'),
    path('layout/', views.layout.layout_list, name='layout_list'),
    path('layout/new/', views.layout.layout_new, name='layout_new'),
    path('layout/<int:layout_id>/', views.layout.layout_detail, name='layout_detail'),
    path('layout/<int:layout_id>/edit/', views.layout.layout_edit, name='layout_edit'),
    path('layout/<int:layout_id>/delete/', views.layout.layout_delete, name='layout_delete'),

    # seat
    path('seat/', views.seat.seat_list, name='seat_list'),
    path('seat/place/<int:layout_id>/', views.seat.seat_place, name='seat_place'),
    path('seat/sit/<int:layout_id>/', views.seat.seat_sit, name='seat_sit'),
    path('seat/view/<int:layout_id>/', views.seat.seat_view, name='seat_view'),

    # usage
    path('usage/', views.usage.usage_list, name='usage_list'),
    
    # usagelog
    path('usagelog/', views.usagelog.usagelog_list, name='usagelog_list'),
]
