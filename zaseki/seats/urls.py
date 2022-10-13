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
    path('layout/place/<int:layout_id>/', views.layout.layout_place, name='layout_place'),
    path('layout/sit/<int:layout_id>/', views.layout.layout_sit, name='layout_sit'),
    path('layout/view/<int:layout_id>/', views.layout.layout_view, name='layout_view'),

    # seat
    path('seat/', views.seat.seat_list, name='seat_list'),
    path('seat/<int:seat_id>/', views.seat.seat_detail, name='seat_detail'),
    path('seat/<int:seat_id>/locate/', views.seat.seat_locate, name='seat_locate'),

    # usage
    path('usage/', views.usage.usage_list, name='usage_list'),
    
    # usagelog
    path('usagelog/', views.usagelog.usagelog_list, name='usagelog_list'),
]
