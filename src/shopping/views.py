import logging

from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Product, OrderItem
from .services.cart_services import process_cart
from .services.order_services import get_order_details

logger = logging.getLogger(__name__)


def display_products(request):
    """ This view renders full list of products """
    products = Product.objects.all()
    return render(request, 'display_products.html', {'products': products})


def render_products_div(request):
    """ This view renders HTMX products_list.html """
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})


def display_cart(request):
    """ This view renders shopping cart """
    try:
        orderitems, total_order_price = get_order_details(request)
    except Http404:
        return render(request, 'empty_cart.html', {'message': 'Your cart is empty'})
    return render(request, 'cart_page.html',
                  {'orderitems': orderitems, 'total_order_price': total_order_price})


def render_cart_div(request):
    """ This view renders HTMX actual_cart.html """
    orderitems, total_order_price = get_order_details(request)
    return render(request, 'actual_cart.html',
                  {'orderitems': orderitems, 'total_order_price': total_order_price})


@require_http_methods(['POST'])
def add_product_to_cart(request, id):
    process_cart(request, id)
    return render_products_div(request)


@require_http_methods(['POST'])
def add_product_to_cart_div(request, id):
    process_cart(request, id)
    return render_cart_div(request)


@require_http_methods(['POST'])
def decrease_product_cart_div(request, id):
    process_cart(request, id)
    return render_cart_div(request)


@require_http_methods(['DELETE'])
def remove_from_cart(request, id):
    OrderItem.objects.get(id=id).delete()
    return render_cart_div(request)
