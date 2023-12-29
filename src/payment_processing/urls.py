from django.urls import path

from payment_processing.views import pay_for_order

urlpatterns = [
    path('pay_for_order/', pay_for_order, name='pay_for_order'),
]
