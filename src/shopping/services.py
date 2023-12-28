from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404

from shopping.models import Product, Order, OrderItem


def add_to_cart(request, product_id, quantity):
    """ Main logic of adding product to cart """
    try:
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(user=request.user)
        else:
            order_key = request.session.session_key
            if not order_key:
                request.session.create()
                order_key = request.session.session_key
            order, created = Order.objects.get_or_create(session_key=order_key)

        OrderItem.objects.create(product=product, order=order, quantity=quantity)
        messages.success(request, 'Product added to cart successfully.')
    except ValueError:
        messages.error(request, 'Invalid quantity.')
    except ObjectDoesNotExist:
        messages.error(request, 'Product not found.')


def get_order(request):
    """ Getting an order object from database for either authorized user or using session-based user """
    if request.user.is_authenticated:
        order = get_object_or_404(Order, user=request.user)
    else:
        order_key = request.session.session_key
        if not order_key:
            raise Http404
        order = get_object_or_404(Order, session_key=order_key)
    return order
