import os
import uuid

from yookassa import Configuration, Payment as YooPayment

from payment_processing.models import Payment


def create_payment(order):
    """ Main logic for creating payment object using YOOKASSA LIB """
    Configuration.configure(os.environ.get('KASSA_ACC_ID'), os.environ.get('KASSA_SECRET_KEY'))
    idempotence_key = str(uuid.uuid4())
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
        "description": f'Платеж по заказу номер {order.uuid}'
    }, idempotence_key)
    payment = Payment.objects.create(
        order=order,
        yoo_id=yoo_payment.id,
        status=yoo_payment.status,
        amount=yoo_payment.amount.value,
        currency=yoo_payment.amount.currency,
        confirmation_url=yoo_payment.confirmation.confirmation_url
    )
    return payment
