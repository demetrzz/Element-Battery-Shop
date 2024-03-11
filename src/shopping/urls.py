from django.urls import path

from shopping.views import display_products, add_product_to_cart, display_cart, add_product_to_cart_div, \
    decrease_product_cart_div, remove_from_cart, display_reviews, leave_review, submit_review, display_orders

urlpatterns = [
    path('', display_products, name='display_products'),
    path('cart/', display_cart, name='display_cart'),
    path('orders/', display_orders, name='display_orders'),
    path('products/<int:id>/add_product_to_cart/', add_product_to_cart, name='add_product_to_cart'),
    path('products/<int:id>/add_product_to_cart_div/', add_product_to_cart_div, name='add_product_to_cart_div'),
    path('products/<int:id>/decrease_product_cart_div/', decrease_product_cart_div, name='decrease_product_cart_div'),
    path('products/<int:id>/remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('products/<int:id>/product_reviews/', display_reviews, name='product_reviews'),
    path('products/<int:id>/leave_review/', leave_review, name='leave_review'),
    path('products/<int:id>/submit_review/', submit_review, name='submit_review'),
]
