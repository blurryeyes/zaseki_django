from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _

from .models import User
from .forms import MyUserChangeAdminForm, MyUserCreationAdminForm

# class MyUserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = '__all__'

# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         # ユーザ登録に必要な項目
#         fields = ('employee_number', 'email',)

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('employee_number', 'password')}),
        (_('Personal info'), {'fields': ('email', 'last_name', 'first_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('employee_number', 'email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeAdminForm
    add_form = MyUserCreationAdminForm
    list_display = ('employee_number', 'email', 'last_name', 'first_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'last_name', 'first_name')
    ordering = ('employee_number',)

admin.site.register(User, MyUserAdmin)