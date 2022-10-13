from asyncio.log import logger
from cmath import log
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import MyUserChangeForm, MyUserInitialSettingForm
from .models import User
from seats.models import Usage, UsageLog


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
            logger.info("姓名が設定されました。")
            return redirect('top')
    else:
        form = MyUserInitialSettingForm(instance=login_user)
    params = {
        'form' : form,
        }
    return render(request, 'accounts/initial_setting.html', params)


@login_required
def account_detail(request):
    """
    自身のユーザー情報を照会

    Parameters
    ----------
    request : HttpRequest

    Templates
    -------
    照会ページ : accounts/account_detail.html
    """
    id = request.user.id
    user = User.objects.get(id=id)
    params = {
        'user' : user,
        }
    return render(request, 'accounts/account_detail.html', params)


@login_required
def account_edit(request):
    """
    自身のユーザー情報を編集

    Parameters
    ----------
    request : HttpRequest

    Templates
    -------
    編集ページ : accounts/account_edit.html
    保存後の遷移先 : account_detail
    """
    id = request.user.id
    user = User.objects.get(id=id)
    if request.method == 'POST':
        form = MyUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account_detail')
    else:
        form = MyUserChangeForm(instance=user)
    params = {
        'user' : user,
        'form' : form
        }
    return render(request, 'accounts/account_edit.html', params)


def user_list(request):
    users = User.objects.order_by('id').all()
    employee_number = request.GET.get('employee_number')
    if employee_number is not None:
        users = users.filter(employee_number=employee_number)
    last_name = request.GET.get('last_name')
    if last_name is not None:
        users = users.filter(last_name__contains=last_name)
    first_name = request.GET.get('first_name')
    if first_name is not None:
        users = users.filter(first_name__contains=first_name)
    params = {
        'users' : users,
        }
    return render(request, 'accounts/user_list.html', params)


@login_required
def user_detail(request, user_id):
    display_user = User.objects.filter(id=user_id).first()
    usages = Usage.objects.select_related('user').select_related('seat__layout').filter(user=user_id).order_by('sit_datetime')
    usagelogs = UsageLog.objects.select_related('user').select_related('seat__layout').filter(user=user_id).order_by('sit_datetime')
    params = {
        # 変数名「user」はbase.htmlと被るので違う名前にすること
        'display_user' : display_user,
        'usages' : usages,
        'usagelogs' : usagelogs,
        }
    return render(request, 'accounts/user_detail.html', params)
