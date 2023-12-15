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
    email = models.EmailField(verbose_name='Почта покупателя', blank=True)
    items_cost = models.IntegerField(default=0, verbose_name='Стоимость товаров')

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


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')