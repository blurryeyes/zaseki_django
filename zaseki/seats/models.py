from asyncio.log import logger
from cmath import log
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

from zaseki.myutils import format_dhms

import logging
import os
# import uuid

from zaseki.settings import MEDIA_ROOT

logger = logging.getLogger('django')


class Layout(models.Model):
    def get_image_path(self, filename):
        """カスタマイズした画像パスを取得する.
        https://qiita.com/kojionilk/items/da20c732642ee7377a78
        
        Parameters
        ----------
        self : インスタンス(models.Model)
        filename : 元のファイル名

        Returns
        -------
        str
            カスタマイズしたファイル名を含む画像パス
        """
        # prefix = 'image/'
        prefix = ''
        # name = str(uuid.uuid4()).replace('-', '')
        name = timezone.localtime(timezone.now()).strftime('%Y%m%d%H%M%S')
        extension = os.path.splitext(filename)[-1]
        return prefix + name + extension
    
    def delete_previous_file(function):
        """不要となる古いファイルを削除する為のデコレータ実装

        Parameters
        ----------
        function : メイン関数

        Returns
        -------
            wrapper
        """
        def wrapper(*args, **kwargs):
            """Wrapper 関数

            Returns
            -------
                メイン関数実行結果
            """
            self = args[0]
            
            # 保存前のファイル名を取得
            result = Layout.objects.filter(pk=self.pk)
            previous = result[0].image.name if len(result) else None
            present = self.image.name
            super(Layout, self).save()

            # 関数実行
            result = function(*args, **kwargs)

            # 保存前のファイルがあったら削除
            if previous is not None and previous != present:
                os.remove(MEDIA_ROOT + '/' + previous)
            return result
        return wrapper
    
    layout_name = models.CharField(verbose_name='レイアウト名', max_length=100) # デフォルトblank=False, null=False
    layout_width = models.IntegerField(verbose_name='レイアウト横幅(px)', validators=[MinValueValidator(0), MaxValueValidator(9999)])
    layout_height = models.IntegerField(verbose_name='レイアウト縦幅(px)', validators=[MinValueValidator(0), MaxValueValidator(9999)])
    seat_width = models.IntegerField(verbose_name='座席横幅(px)', validators=[MinValueValidator(0), MaxValueValidator(999)])
    seat_height = models.IntegerField(verbose_name='座席縦幅(px)', validators=[MinValueValidator(0), MaxValueValidator(999)])
    font_size = models.IntegerField('フォントサイズ(px)', validators=[MinValueValidator(0), MaxValueValidator(99)])
    opacity = models.DecimalField(verbose_name='不透明度', decimal_places=2, max_digits=3, validators=[MinValueValidator(0), MaxValueValidator(1)], default=0.8)
    non_sitting_seat_color = models.CharField(verbose_name="空席(色)", max_length=7, validators=[RegexValidator(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$')], default="#25C964")
    sitting_seat_color = models.CharField(verbose_name="満席(色)", max_length=7, validators=[RegexValidator(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$')], default="#FF6699")
    notice = models.TextField(verbose_name='注意事項', max_length=1000, blank=True, null=False)
    # image = models.ImageField(verbose_name='レイアウト画像', upload_to='')
    image = models.ImageField(verbose_name='レイアウト画像', upload_to=get_image_path)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作成者', on_delete=models.SET_NULL, null=True, related_name='layout_created_by')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='更新者', on_delete=models.SET_NULL, null=True, related_name='layout_updated_by')

    class Meta:
        verbose_name_plural = 'レイアウト'

    def __str__(self):
        return self.layout_name
    
    @delete_previous_file
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Layout, self).save()

    @delete_previous_file
    def delete(self, using=None, keep_parents=False):
        super(Layout, self).delete()


class Seat(models.Model):
    x_coordinate = models.DecimalField(verbose_name='X座標(px)', decimal_places=2, max_digits=6, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    y_coordinate = models.DecimalField(verbose_name='Y座標(px)', decimal_places=2, max_digits=6, validators=[MinValueValidator(0), MaxValueValidator(9999)])
    is_used = models.BooleanField(verbose_name='使用中', default=False)
    layout = models.ForeignKey(Layout, verbose_name='レイアウト', on_delete=models.SET_NULL, null=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='使用者', through='Usage')
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作成者',on_delete=models.SET_NULL, null=True, related_name='seat_created_by')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='更新者', on_delete=models.SET_NULL, null=True, related_name='seat_updated_by')

    class Meta:
        verbose_name_plural = '座席'

    def __str__(self):
        layout_name = self.layout.layout_name if self.layout is not None else '存在しないレイアウト'
        return 'ID:' + str(self.id) + ' レイアウト:' + layout_name + ' X座標:' + str(self.x_coordinate) + ' Y座標:' + str(self.y_coordinate)

    # @classmethod
    # def get_model_fields(cls):
    #     """
    #         フィールド名を取得する関数
    #         https://www.memory-lovers.blog/entry/2020/05/18/144153
    #     """
    #     # クラスに定義されているフィールド名を取得
    #     meta_fields = cls._meta.get_fields()

    #     # 全部取得してしまうので、必要なものだけにフィルタリング
    #     # related_nameを指定しているmodels.ForeignKeyがあると、
    #     # models.ManyToOneRelのフィールドが作成されるので除外する
    #     filtered_fields = filter(
    #         lambda x: not isinstance(x, models.ManyToOneRel),
    #         meta_fields
    #     )
      
    #     # フィルタリングしたフィールドからフィールド名に変換
    #     meta_field_names = map(lambda x: x.name, filtered_fields)
    #     return list(meta_field_names)

    def delete(self, *args, **kwargs):
        usage = None
        try:
            usage = Usage.objects.get(seat = self.id)
        except:
            logger.info("紐づく利用状況はありません。")
            pass
        else:
            logger.info("紐づく利用状況があります。")
            usage.delete()
        super(Seat, self).delete(*args, **kwargs)


class Usage(models.Model):
    seat = models.OneToOneField(Seat, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    sit_datetime = models.DateTimeField(verbose_name='着席日時', auto_now_add=True)
    
    class Meta:
        verbose_name_plural = '利用状況'
    
    def save(self, *args, **kwargs):
        self.seat.is_used = True
        self.seat.save()
        super(Usage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.seat.is_used = False
        self.seat.save()
        super(Usage, self).delete(*args, **kwargs)
        print('delete Usage')
        UsageLog(
            x_coordinate=self.seat.x_coordinate,
            y_coordinate=self.seat.y_coordinate,
            layout=self.seat.layout,
            seat=self.seat,
            user=self.user,
            sit_datetime=self.sit_datetime,
            leave_datetime=timezone.now()
            ).save()
        return self
    
    def __str__(self):
        return '座席ID:' + str(self.seat.id) + ' 使用者:' + self.user.email
    
    def sitting_time(self):
        sitting_time = timezone.now() - self.sit_datetime
        format_sitting_time = format_dhms(sitting_time.days, sitting_time.seconds)
        return format_sitting_time


class UsageLog(models.Model):
    x_coordinate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    y_coordinate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999)])
    layout = models.ForeignKey(Layout, on_delete=models.SET_NULL, null=True)
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    sit_datetime = models.DateTimeField(verbose_name='着席日時', blank=True, null=True)
    leave_datetime = models.DateTimeField(verbose_name='離席日時', blank=True, null=True)
    # is_batch_worked = models.BooleanField(defaut=False)

    class Meta:
       verbose_name_plural = '利用履歴'

    def sitting_time(self):
        sitting_time = self.leave_datetime - self.sit_datetime
        format_sitting_time = format_dhms(sitting_time.days, sitting_time.seconds)
        return format_sitting_time
