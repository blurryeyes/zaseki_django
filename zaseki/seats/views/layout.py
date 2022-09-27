from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

import logging

from seats.forms import LayoutForm
from seats.models import Layout

logger = logging.getLogger('django')


def top(request):
    return redirect('layout_list')


def layout_list(request):
    login_user = request.user
    if login_user.is_authenticated:
        # 姓名が設定されていない場合は設定画面へ
        if not login_user.last_name or not login_user.first_name:
            return redirect('initial_setting')
    layouts = Layout.objects.prefetch_related('created_by').order_by('id').all()
    layout_name = request.GET.get('layout_name')
    if layout_name is not None:
        layouts = layouts.filter(layout_name__contains=layout_name)
    # トップページへ
    return render(request, 'seats/layout_list.html', {"layouts": layouts})


@login_required
@user_passes_test(lambda user: user.is_staff)
def layout_new(request):
    # https://qiita.com/j54854/items/1f0560142e39d888251c
    if request.method == 'POST':
        # 画像情報はrequest.POSTに持っていないかつ、画像はblank=False null=Falseであるため、is_valid前にformに設定する必要がある
        form = LayoutForm(request.POST, request.FILES)
        if form.is_valid():
            layout = form.save(commit=False)
            # layout.image = request.FILES['image'] blank=True null=Trueならここでもいい
            layout.created_by = request.user
            layout.updated_by = request.user
            layout.updated_at = timezone.now
            layout.save()
            logger.info("レイアウトを作成しました。")
            return redirect('layout_list')
    else:
        form = LayoutForm()
    return render(request, 'seats/layout_new.html', {'form' : form})


@login_required
@user_passes_test(lambda user: user.is_staff)
def layout_edit(request, layout_id):
    layout = get_object_or_404(Layout, pk=layout_id)
    if request.method == 'POST':
        form = LayoutForm(request.POST, request.FILES, instance=layout)
        if form.is_valid():
            layout = form.save(commit=False)
            layout.updated_by = request.user
            layout.updated_at = timezone.now
            layout.save()
            logger.info("レイアウトを更新しました。")
            return redirect('layout_detail', layout_id=layout_id)
    else:
        form = LayoutForm(instance=layout)
    return render(request, 'seats/layout_edit.html', {'form' : form})


def layout_detail(request, layout_id):
    layout = get_object_or_404(Layout, pk=layout_id)
    # TODO:ユーザ2回呼んでる
    # layout = Layout.objects.prefetch_related('created_by').prefetch_related('updated_by').filter(pk=layout_id).first()
    return render(request, "seats/layout_detail.html", {"layout": layout})


@login_required
@user_passes_test(lambda user: user.is_staff)
def layout_delete(request, layout_id):
    layout = get_object_or_404(Layout, pk=layout_id)
    try:
        layout.delete()
    except:
        logger.error("レイアウト削除に失敗しました。")
    return redirect('layout_list')
