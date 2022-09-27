from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import CreateView

from accounts import views, admin

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('signup/', CreateView.as_view(template_name='accounts/signup.html', form_class=admin.MyUserCreationAdminForm, success_url='/'), name='signup'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('init/', views.initial_setting, name='initial_setting'),
    path('detail/', views.user_detail, name='user_detail'),
    path('list/', views.user_list, name='user_list'),
    path('edit/', views.user_edit, name='user_edit'),
]
