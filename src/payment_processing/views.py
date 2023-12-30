from django.http import Http404
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from payment_processing.services import create_payment


@require_http_methods(['POST'])
def pay_for_order(request):
    try:
        payment = create_payment(request)
    except Http404:
        raise
    return redirect(str(payment.confirmation_url))
