# from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User

class MyUserChangeAdminForm(UserChangeForm):
    """
    管理ページ用
    """
    class Meta:
        model = User
        fields = '__all__'

class MyUserCreationAdminForm(UserCreationForm):
    """
    管理ページ用
    """
    class Meta:
        model = User
        # ユーザ登録に必要な項目
        fields = ('employee_number', 'email',)

# class MyUserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('email', 'last_name', 'first_name',)
class MyUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
        # form.as_tableのときにコロンを表示させない
        # https://www.maytisk.com/django-form-no-colon/

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # ユーザ登録に必要な項目
        fields = ('employee_number', 'email',)

class MyUserInitialSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name']