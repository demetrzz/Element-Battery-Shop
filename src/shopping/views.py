import logging

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Product
from .services import add_to_cart, get_order

logger = logging.getLogger(__name__)


def display_products(request):
    products = Product.objects.all()
    return render(request, 'display_products.html', {'products': products})


def display_cart(request):
    order = get_order(request)
    orderitems = order.items.all().values('product__name', 'product__price', 'quantity')
    total_order_price = order.get_total()
    return render(request, 'cart.html',
                  {'orderitems': orderitems, 'total_order_price': total_order_price})


@require_http_methods(['POST'])
def add_product_to_cart(request, id):
    logger.info('posting product to order')
    quantity = request.POST.get('quantity', 1)
    try:
        quantity = int(quantity)
        if quantity < 1:
            messages.error(request, 'Quantity must be at least 1.')
            return HttpResponse(status=400)
        add_to_cart(request, id, quantity)
        return HttpResponse('<p class="success">Product added to cart successfully.</p>')
    except ValueError:
        messages.error(request, 'Invalid quantity.')
        return HttpResponse('<p class="error">Invalid quantity.</p>', status=400)
