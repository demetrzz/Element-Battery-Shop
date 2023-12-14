from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.FileField(upload_to='items/', null=True, blank=True, verbose_name='Изображение')
    quantity_in_stock = models.PositiveIntegerField(default=0, blank=True, verbose_name='Количество на складе')

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item, through='OrderItem')
    customer_name = models.CharField(max_length=200, verbose_name='Имя покупателя', blank=True)
    email = models.EmailField(verbose_name='Почта покупателя', blank=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон покупателя', blank=True)
    items_cost = models.IntegerField(default=0, verbose_name='Стоимость товаров')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
