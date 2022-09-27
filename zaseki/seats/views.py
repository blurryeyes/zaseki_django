from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

import logging

from .forms import LayoutForm
from .models import Layout, Seat, Usage, UsageLog

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


@login_required
@user_passes_test(lambda user: user.is_staff)
def seat_place(request, layout_id):
    view_type = 'place'
    logger.info("レイアウトを取得します。")
    layout = get_object_or_404(Layout, pk=layout_id)
    logger.info("レイアウトを取得しました。")
    if request.method == 'POST':
        x_coordinate = request.POST.get('x')
        y_coordinate = request.POST.get('y')
        seat_id = request.POST.get('seat_id')
        # 座席の削除(DELETE)
        if x_coordinate is None or y_coordinate is None:
            logger.info("座席を削除します。")
            seat = get_object_or_404(Seat, pk=int(seat_id))
            seat.delete()
            logger.info("座席を削除しました。")
        # 座席の新規配置(CREATE)
        elif seat_id == 'new':
            logger.info("座席を設置します。")
            seat = Seat(layout = get_object_or_404(Layout, pk=layout_id),
                        x_coordinate = float(x_coordinate),
                        y_coordinate = float(y_coordinate),
                        created_by = request.user,
                        updated_by = request.user,
                        updated_at = timezone.now
                        )
            seat.save()
            logger.info("座席を設置しました。")
        # 座席の移動(UPDATE)
        else:
            logger.info("座席を配置換えします。")
            seat = get_object_or_404(Seat, pk=int(seat_id))
            seat.x_coordinate = float(x_coordinate)
            seat.y_coordinate = float(y_coordinate)
            seat.updated_by = request.user
            seat.updated_at = timezone.now
            seat.save()
            logger.info("座席を配置換えしました。")

    logger.info("座席を取得します。")
    # https://chuna.tech/detail/49/
    seats = Seat.objects.prefetch_related('user').filter(layout=layout_id)
    logger.info("座席を取得しました。")
    # TODO:縦横比より短い辺を基準に表示する画像サイズを決定
    return render(request, 'seats/seat_base.html', {'view_type': view_type, 'layout': layout, 'seats': seats})


@login_required
def seat_sit(request, layout_id):
    view_type = 'sit'
    logger.info("レイアウトを取得します。")
    layout = get_object_or_404(Layout, pk=layout_id)
    logger.info("レイアウトを取得しました。")
    user = request.user
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')

        # 座席の処理
        sitting(user, layout, seat_id)

    logger.info("座席を取得します。")
    # https://chuna.tech/detail/49/
    seats = Seat.objects.prefetch_related('user').filter(layout=layout_id)
    logger.info("座席を取得しました。")
    return render(request, 'seats/seat_base.html', {'view_type': view_type, 'layout': layout, 'seats': seats})


def sitting(user, layout, seat_id):
    """座席の処理

    Parameters
    ----------
    user : request.user
    layout : 表示中のレイアウト
    seat_id : 利用しようとしている座席ID
    """
    with transaction.atomic():
        previous_seat_usage = Usage.objects.filter(seat_id=int(seat_id)).first()
        # その座席に直前まで座っていたユーザーのID
        previous_user_id = previous_seat_usage.user.id if previous_seat_usage is not None else None

        # ぞの座席に誰か座っていた（新規保存処理なし）
        if previous_user_id is not None:
            # 座っていたのは自分
            if previous_user_id == user.id:
                logger.info("離席します。")
                previous_seat_usage.delete()
                logger.info("離席しました。")
            else:
                logger.info("別ユーザーが利用中です。")
        
        # その座席は空席だった（新規保存処理あり）
        else:
            # 自分がこのレイアウト上で直前まで座っていた座席の利用状況
            previous_usage = Usage.objects.filter(user=user, seat__layout=layout).first()
            # 同じレイアウト内の席から移動してきた
            if previous_usage is not None:
                logger.info("古い利用状況を削除します。")
                previous_usage.delete()
                logger.info("古い利用状況を削除しました。")
            # 同じレイアウト内に座った経歴なし。
            else:
                logger.info("古い利用状況ありません。")
            # その座席の座席情報
            present_seat = get_object_or_404(Seat, pk=int(seat_id))
            present_usage = Usage(seat=present_seat, user=user)
            logger.info("利用状況を設定します。")
            present_usage.save()
            logger.info("利用状況を設定しました。")


def seat_view(request, layout_id):
    view_type = 'view'
    logger.info("レイアウトを取得します。")
    layout = get_object_or_404(Layout, pk=layout_id)
    logger.info("レイアウトを取得しました。")
    logger.info("座席を取得します。")
    # https://chuna.tech/detail/49/
    seats = Seat.objects.prefetch_related('user').filter(layout=layout_id)
    logger.info("座席を取得しました。")
    return render(request, 'seats/seat_base.html', {'view_type': view_type, 'layout': layout, 'seats': seats})


@login_required
def seat_list(request):
    seats = Seat.objects.select_related('layout').order_by('id').all()
    layout_name = request.GET.get('layout_name')
    if layout_name is not None:
        seats = seats.filter(layout__layout_name__contains=layout_name)
    return render(request, 'seats/seat_list.html', {'seats' : seats})


@login_required
def usage_list(request):
    usages = Usage.objects.prefetch_related('user').order_by('id').all()
    last_name = request.GET.get('last_name')
    if last_name is not None:
        usages = usages.filter(user__last_name__contains=last_name)
    first_name = request.GET.get('first_name')
    if first_name is not None:
        usages = usages.filter(user__first_name__contains=first_name)
    return render(request, 'seats/usage_list.html', {'usages' : usages})


@login_required
def usagelog_list(request):
    usagelogs = UsageLog.objects.prefetch_related('user').order_by('id').all()
    last_name = request.GET.get('last_name')
    if last_name is not None:
        usagelogs = usagelogs.filter(user__last_name__contains=last_name)
    first_name = request.GET.get('first_name')
    if first_name is not None:
        usagelogs = usagelogs.filter(user__first_name__contains=first_name)
    return render(request, 'seats/usagelog_list.html', {'usagelogs' : usagelogs})