from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import CreateView

from accounts import views, admin

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('signup/', CreateView.as_view(template_name='accounts/signup.html', form_class=admin.MyUserCreationAdminForm, success_url='/'), name='signup'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('init/', views.initial_setting, name='initial_setting'),
    path('detail/', views.account_detail, name='account_detail'),
    path('edit/', views.account_edit, name='account_edit'),
    path('user/<int:user_id>/', views.other_user_detail, name='other_user_detail'),
]
