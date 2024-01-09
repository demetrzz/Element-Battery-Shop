import ipaddress
import json

from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from payment_processing.services.payment_services import create_payment, handle_payment_status_change


@require_http_methods(['POST'])
def pay_for_order(request):
    try:
        payment = create_payment(request)
    except Http404:
        raise
    return redirect(str(payment.confirmation_url))


YOOKASSA_IP_ADDRESSES = [
    ipaddress.ip_network('185.71.76.0/27'),
    ipaddress.ip_network('185.71.77.0/27'),
    ipaddress.ip_network('77.75.153.0/25'),
    ipaddress.ip_network('77.75.156.11/32'),
    ipaddress.ip_network('77.75.156.35/32'),
    ipaddress.ip_network('77.75.154.128/25'),
    ipaddress.ip_network('2a02:5180::/32'),
]


@csrf_exempt
@require_http_methods(['POST'])
def yookassa_webhook(request):
    # Get the client's IP address
    ip = ipaddress.ip_address(request.META.get('HTTP_X_FORWARDED_FOR', ''))
    print(ip)
    # Check if the IP address is in YOOKASSA_IP_ADDRESSES
    if not any(ip in net for net in YOOKASSA_IP_ADDRESSES):
        return HttpResponseForbidden('Forbidden')

    # Parse the JSON data from the request body
    data = json.loads(request.body)

    # Handle the payment status change
    handle_payment_status_change(data)

    # Return a 200 OK response
    return HttpResponse(status=200)
