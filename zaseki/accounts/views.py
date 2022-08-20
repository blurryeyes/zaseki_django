from cmath import log
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import MyUserChangeForm, MyUserInitialSettingForm
from .models import User

def hello(request):
    return render(request, 'accounts/hello.html')

@login_required
def initial_setting(request):
    """
    会員登録後に姓名設定

    Parameters
    ----------
    request : HttpRequest

    Templates
    -------
    設定ページ : accounts/initial_setting.html
    姓名設定済みの遷移先 : top
    """
    login_user = request.user
    is_initial_set = login_user.last_name and login_user.first_name
    # 姓名設定済みでこの画面に遷移した場合はトップページへ
    if is_initial_set:
        return redirect('top')
    if request.method == 'POST':
        form = MyUserInitialSettingForm(request.POST, instance=login_user)
        if form.is_valid():
            form.save()
            return redirect('top')
    else:
        form = MyUserInitialSettingForm(instance=login_user)
    return render(request, 'accounts/initial_setting.html', {'form' : form})

@login_required
def account_detail(request):
    """
    自身の会員情報を照会

    Parameters
    ----------
    request : HttpRequest

    Templates
    -------
    照会ページ : accounts/account_detail.html
    """
    # login_user = request.user
    id = request.user.id
    user = User.objects.get(id=id)
    return render(request, 'accounts/account_detail.html', {'user' : user})

@login_required
def account_edit(request):
    """
    自身の会員情報を編集

    Parameters
    ----------
    request : HttpRequest

    Templates
    -------
    編集ページ : accounts/account_edit.html
    保存後の遷移先 : account_detail
    """
    # login_user = request.user
    id = request.user.id
    user = User.objects.get(id=id)
    # employee_number = user.employee_number
    if request.method == 'POST':
        form = MyUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account_detail')
    else:
        form = MyUserChangeForm(instance=user)
    return render(request, 'accounts/account_edit.html', {'user' : user, 'form' : form})