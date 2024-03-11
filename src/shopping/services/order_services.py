from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404

from shopping.models import Order, Product, OrderItem


@transaction.atomic
def get_or_create_order(request):
    """ Get or create order """
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status=Order.CREATED).first()
        if order is None:
            order = Order.objects.create(user=request.user)
    else:
        order_key = request.session.session_key
        if not order_key:
            request.session.create()
            order_key = request.session.session_key
        order = Order.objects.filter(session_key=order_key, status=Order.CREATED).first()
        if order is None:
            order = Order.objects.create(session_key=order_key)
    return order


def get_product(product_id):
    """ Get product """
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")


@transaction.atomic
def get_or_create_orderitem(product, order, quantity):
    """ Get or create order item """
    orderitem, created = OrderItem.objects.get_or_create(
        product=product,
        order=order,
    )
    if quantity + orderitem.quantity > product.quantity_in_stock:
        raise ValueError("Not enough stock")
    return orderitem


@transaction.atomic
def update_orderitem_quantity(orderitem, quantity):
    """ Update quantity """
    orderitem.quantity = F('quantity') + quantity
    orderitem.save(update_fields=['quantity'])
    orderitem.refresh_from_db()
    if orderitem.quantity <= 0:
        orderitem.delete()


def get_order_details(request):
    """ This function gets the order details """
    # Getting an order object from database for either authorized user or using session-based user
    if request.user.is_authenticated:
        order = get_object_or_404(Order.objects.filter(status=Order.CREATED).select_related('user'), user=request.user)
    else:
        order_key = request.session.session_key
        if not order_key:
            raise Http404("Order does not exist")
        order = get_object_or_404(Order.objects.filter(status=Order.CREATED), session_key=order_key)

    # Getting the order details
    orderitems = order.items.select_related('product')

    total_order_price = order.get_total()
    return orderitems, total_order_price


def get_orders_by_user(request):
    """ Get or create order """
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        order_key = request.session.session_key
        orders = Order.objects.filter(session_key=order_key)
    return orders
