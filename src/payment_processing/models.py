from django.db import models

from shopping.models import Order


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ')
    yoo_id = models.CharField(max_length=200, null=True, verbose_name='ID в YooKassa')

    PENDING = 'pending'
    WAITING_FOR_CAPTURE = 'waiting_for_capture'
    SUCCEEDED = 'succeeded'
    CANCELED = 'canceled'
    STATUS_CHOICES = [
        (PENDING, 'Ожидает оплаты'),
        (WAITING_FOR_CAPTURE, 'Оплачен, ожидает подтверждения'),
        (SUCCEEDED, 'Оплачен и подтвержден'),
        (CANCELED, 'Отменен')
    ]
    currency = models.CharField(max_length=3, default='RUB', verbose_name='Валюта платежа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, db_index=True, verbose_name='Статус платежа')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма платежа')
    confirmation_url = models.CharField(max_length=200, null=True, verbose_name='URL подтверждения')
