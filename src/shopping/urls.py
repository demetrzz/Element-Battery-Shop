from django.urls import path

from shopping.views import display_products, delete_product, add_product_to_cart

urlpatterns = [
    path('products/', display_products, name='display_tasks'),
    path('products/<int:id>/delete/', delete_product, name='delete_product'),
    path('products/<int:id>/post/', add_product_to_cart, name='add_product_to_cart'),

]