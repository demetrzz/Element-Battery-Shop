import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from .models import Product, OrderItem, Order

logger = logging.getLogger(__name__)


def display_products(request):
    products = Product.objects.all()
    return render(request, 'display_products.html', {'products': products})


@require_http_methods(['DELETE'])
def delete_product(request, id):
    Product.objects.filter(id=id).delete()
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})


@require_http_methods(['POST'])
def add_product_to_cart(request, id):
    logger.info('posting product to order')
    try:
        quantity = request.POST.get('quantity', 1)
        quantity = int(quantity)
        if quantity < 1:
            return HttpResponse('<p class="error">Quantity must be at least 1.</p>', status=400)

        product = get_object_or_404(Product, id=id)

        if request.user.is_authenticated:
            order, created = Order.objects.get_or_create(user=request.user)
        else:
            order_key = request.session.session_key
            if not order_key:
                request.session.create()
                order_key = request.session.session_key
            order, created = Order.objects.get_or_create(session_key=order_key)

        OrderItem.objects.create(product=product, order=order, quantity=quantity)

        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'message.html', {'message': 'Product added to cart successfully.'})

        return HttpResponse('<p class="success">Product added to cart successfully.</p>')

    except ValueError:
        return HttpResponse('<p class="error">Invalid quantity.</p>', status=400)
    except ObjectDoesNotExist:
        return HttpResponse('<p class="error">Product not found.</p>', status=404)
