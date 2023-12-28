from django.test import TestCase
from ..models import Product, Order, OrderItem


class ModelsTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(
            name='Test Product 1',
            price=100.00,
            description='Test Description 1',
            quantity_in_stock=10
        )

        self.product2 = Product.objects.create(
            name='Test Product 2',
            price=200.00,
            description='Test Description 2',
            quantity_in_stock=20
        )

        self.order = Order.objects.create()

        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            quantity=2
        )

        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            quantity=3
        )

    def test_get_cost(self):
        self.assertEqual(self.order_item1.get_cost(), 200.00)
        self.assertEqual(self.order_item2.get_cost(), 600.00)

    def test_get_total(self):
        self.assertEqual(self.order.get_total(), 800.00)

    def test_order_status(self):
        self.assertEqual(self.order.status, Order.CREATED)
        self.order.status = Order.PAID
        self.order.save()
        self.assertEqual(self.order.status, Order.PAID)
