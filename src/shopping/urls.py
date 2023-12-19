from django.urls import path

from shopping.views import display_products, add_product_to_cart, display_cart

urlpatterns = [
    path('products/', display_products, name='display_products'),
    path('cart/', display_cart, name='display_cart'),
    path('products/<int:id>/post/', add_product_to_cart, name='add_product_to_cart'),
]
