from django.conf import settings
from django.db import models
from django.utils import timezone


class Store(models.Model):
    """店舗"""
    name = models.CharField('店名', max_length=255)

    def __str__(self):
        return self.name


class Staff(models.Model):
    """店舗スタッフ"""
    name = models.CharField('表示名', max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='ログインユーザー', on_delete=models.CASCADE
    )
    store = models.ForeignKey(Store, verbose_name='店舗', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'store'], name='unique_staff'),
        ]

    def __str__(self):
        return f'{self.store.name} - {self.name}'


class Schedule(models.Model):
    """予約スケジュール."""
    start = models.DateTimeField('開始時間')
    end = models.DateTimeField('終了時間')
    date = models.CharField('予約日(mm/dd)', max_length=10, null=True)
    name = models.CharField('予約者', max_length=255)
    grade  = models.CharField('回生',max_length=1)
    band = models.CharField('予約バンド', max_length=200)
    staff = models.ForeignKey('Staff', verbose_name='スタッフ', on_delete=models.CASCADE)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.date} {self.name} {self.grade} {self.band} {start} ~ {end} {self.staff}'
