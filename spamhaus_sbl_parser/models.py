from django.db import models
from django.utils.translation import ugettext_lazy as _


class SblLog(models.Model):

    msg = models.TextField(verbose_name=_('Сообщение'), blank=True, default='')
    date_create = models.DateTimeField(verbose_name=_('Дата создания'), auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.msg

    class Meta:
        verbose_name = _('Лог')
        verbose_name_plural = _('Лог')


class SblItem(models.Model):
    date = models.CharField(verbose_name=_('Дата'), blank=True, null=True, max_length=100)
    network = models.CharField(verbose_name=_('Сеть'), blank=True, null=True, max_length=100)
    ref_name = models.CharField(verbose_name=_('Ref'), blank=True, null=True, max_length=100, unique=True)
    domen = models.CharField(verbose_name=_('Домен'), blank=True, null=True, max_length=100)
    ref_href = models.CharField(verbose_name=_('Детальная ссылка'), blank=True, null=True, max_length=100)
    ptext = models.TextField(verbose_name=_('Короткий текст'), blank=True, null=True, max_length=300)
    ref_detail_text = models.TextField(verbose_name=_('Детальный текст'), null=True, blank=True)
    status = models.CharField(verbose_name=_('Статус'), blank=True, null=True, max_length=20)
    date_create = models.DateTimeField(verbose_name=_('Дата создания'), auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.ref_name

    class Meta:
        verbose_name = _('SBL item')
        verbose_name_plural = _('SBL item')
        ordering = ['-date']
