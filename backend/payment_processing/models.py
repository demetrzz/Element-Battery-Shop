from django.db import models

from shopping.models import Order


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
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

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, db_index=True, verbose_name='Статус платежа')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма платежа')