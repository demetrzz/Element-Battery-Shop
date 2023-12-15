from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Product, OrderItem


def display_products(request):
    products = Product.objects.all()
    return render(request, 'display_products.html', {'products': products})


@require_http_methods(['DELETE'])
def delete_product(request, id):
    Product.objects.filter(id=id).delete()
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})


@csrf_exempt
@require_http_methods(['POST'])
def add_product_to_cart(request, id):
    OrderItem.objects.create(product_id=id, order_id=1)
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})
