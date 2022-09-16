from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from import_export import resources, fields
from import_export.admin import ImportExportMixin

from .models import User
from .forms import MyUserChangeAdminForm, MyUserCreationAdminForm


class UserResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        value = row['password']
        row['password'] = make_password(value)

    class Meta:
        model = User


class MyUserAdmin(ImportExportMixin, UserAdmin):
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

    resource_class = UserResource


admin.site.register(User, MyUserAdmin)