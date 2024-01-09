import os
import uuid

from django.db import transaction
from django.shortcuts import get_object_or_404
from yookassa import Configuration, Payment as YooPayment

from payment_processing.models import Payment
from shopping.models import Order


def create_yoo_payment(order):
    """
    Create a new one-staged YooPayment
    (it goes from pending to succeeded skipping waiting_for capture method)
    can be changed by changing "capture" to False
    """
    return YooPayment.create({
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
    }, str(uuid.uuid4()))


def create_payment_object(order, yoo_payment):
    """ Create a new Payment object """
    return Payment.objects.create(
        order=order,
        yoo_id=yoo_payment.id,
        status=yoo_payment.status,
        amount=yoo_payment.amount.value,
        currency=yoo_payment.amount.currency,
        confirmation_url=yoo_payment.confirmation.confirmation_url
    )


def create_payment(request):
    """ Main logic for creating payment object using YOOKASSA LIB """
    Configuration.configure(os.environ.get('KASSA_ACC_ID'), os.environ.get('KASSA_SECRET_KEY'))
    if request.user.is_authenticated:
        order = get_object_or_404(Order, user=request.user, status='CREATED')
    else:
        session_key = request.session.session_key
        order = get_object_or_404(Order, session_key=session_key, status='CREATED')

    # Check if a payment already exists for the order and is pending
    payment = Payment.objects.filter(order=order, status=Payment.PENDING).order_by('-id').first()

    if payment:
        if order.get_total() != payment.amount:
            # Cancel the existing payment if the order total has changed
            payment.status = Payment.CANCELED
            payment.save()
            # Create a new payment
            yoo_payment = create_yoo_payment(order)
            payment = create_payment_object(order, yoo_payment)
    elif not payment:
        # Create a new payment if no payment exists
        yoo_payment = create_yoo_payment(order)
        payment = create_payment_object(order, yoo_payment)
    return payment


def handle_payment_status_change(data):
    # Extract the payment ID and status from the data
    payment_id = data['object']['id']
    payment_status = data['object']['status']

    # Start a transaction
    with transaction.atomic():
        # Get the Payment object with the given ID
        payment = Payment.objects.select_for_update().get(yoo_id=payment_id)

        # Update the status of the Payment object
        payment.status = payment_status
        payment.save()

        # Get the associated Order object
        order = payment.order

        # Update the status of the Order object based on the payment status
        if payment_status == Payment.SUCCEEDED:
            order.status = Order.PAID

            # Decrement the quantity_in_stock of each Product in the Order
            for item in order.items.all():
                product = item.product
                product.quantity_in_stock -= item.quantity
                product.save()

        elif payment_status == Payment.CANCELED:
            order.status = Order.CANCELED
        # Add more conditions here if needed

        # Save the changes to the Order object
        order.save()
