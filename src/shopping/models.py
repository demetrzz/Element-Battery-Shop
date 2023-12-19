from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование товара')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена единицы товара')
    description = models.TextField(blank=True, verbose_name='Описание товара')
    image = models.FileField(upload_to='products/', null=True, blank=True, verbose_name='Изображение товара')
    quantity_in_stock = models.PositiveIntegerField(default=0, blank=True, verbose_name='Количество товара на складе')

    def __str__(self):
        return self.name


class Order(models.Model):
    products = models.ManyToManyField(Product, through='OrderItem')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=32, null=True, blank=True)

    CREATED = 'CREATED'
    WAITING_PAYMENT = 'WAITING_PAYMENT'
    PAYED = 'PAYED'
    DELIVERY = 'DELIVERY'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    STATUS_CHOICES = [
        (CREATED, 'Создан'),
        (WAITING_PAYMENT, 'Ожидает оплаты'),
        (PAYED, 'Оплачен'),
        (DELIVERY, 'В процессе доставки'),
        (COMPLETED, 'Выполнен'),
        (CANCELED, 'Отменен')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CREATED, verbose_name='Статус')

    def get_total(self):
        total = 0
        for item in self.items.all():
            total += item.get_cost()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def get_cost(self):
        return self.product.price * self.quantity
