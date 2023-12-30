import os
import uuid

from django.shortcuts import get_object_or_404
from yookassa import Configuration, Payment as YooPayment

from payment_processing.models import Payment
from shopping.models import Order


def create_payment(request):
    """ Main logic for creating payment object using YOOKASSA LIB """
    Configuration.configure(os.environ.get('KASSA_ACC_ID'), os.environ.get('KASSA_SECRET_KEY'))
    idempotence_key = str(uuid.uuid4())
    if request.user.is_authenticated:
        order = get_object_or_404(Order, user=request.user, status='CREATED')
    else:
        session_key = request.session.session_key
        order = get_object_or_404(Order, session_key=session_key, status='CREATED')
    yoo_payment = YooPayment.create({
        "amount": {
            "value": str(order.get_total()),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.example.com/return_url"
        },
        "capture": True,
        "description": f'Платеж по заказу номер {order.id}'
    }, idempotence_key)
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            "yoo_id": yoo_payment.id,
            "status": yoo_payment.status,
            "amount": yoo_payment.amount.value,
            "currency": yoo_payment.amount.currency,
            "confirmation_url": yoo_payment.confirmation.confirmation_url}
    )
    return payment
