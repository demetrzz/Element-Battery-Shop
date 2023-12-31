import logging

from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404

from shopping.models import Product, Order, OrderItem


logger = logging.getLogger(__name__)


def process_cart(request, id):
    """ This view handles logic of 'add product to cart' button """
    logger.info('inside process_cart view')
    quantity = request.POST.get('quantity', 1)
    try:
        quantity = int(quantity)
        add_to_cart(request, id, quantity)
        return
    except ValueError:
        messages.error(request, 'Invalid quantity.')
        return HttpResponse('<p class="error">Invalid quantity.</p>', status=400)


def add_to_cart(request, product_id, quantity):
    """ Main logic of adding product to cart """
    logger.info('inside add_to_cart service')
    try:
        with transaction.atomic():
            # Get or create order
            if request.user.is_authenticated:
                order, created = Order.objects.get_or_create(user=request.user)
            else:
                order_key = request.session.session_key
                if not order_key:
                    request.session.create()
                    order_key = request.session.session_key
                order, created = Order.objects.get_or_create(session_key=order_key)

            # Get or create order item
            product = Product.objects.select_for_update().get(id=product_id)
            orderitem, created = OrderItem.objects.select_for_update().get_or_create(
                product=product,
                order=order,
            )

            # Update quantity
            if not created:
                orderitem.quantity = F('quantity') + quantity
                orderitem.save(update_fields=['quantity'])
                orderitem.refresh_from_db()

            # Delete order item if quantity is zero or less
            if orderitem.quantity <= 0:
                orderitem.delete()

    except (ValueError, Product.DoesNotExist) as e:
        messages.error(request, str(e))


def get_order_details(request):
    """ This function gets the order details """
    # Getting an order object from database for either authorized user or using session-based user
    if request.user.is_authenticated:
        order = get_object_or_404(Order.objects.select_related('user'), user=request.user)
    else:
        order_key = request.session.session_key
        if not order_key:
            raise Http404
        order = get_object_or_404(Order.objects.select_related('session_key'), session_key=order_key)

    # Getting the order details
    orderitems = order.items.select_related('product').values('id', 'product__id', 'product__name', 'product__price',
                                                              'quantity')
    total_order_price = order.get_total()
    return orderitems, total_order_price
