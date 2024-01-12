import logging

from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseBadRequest

from shopping.services.exceptions import NotEnoughInStock
from shopping.services.order_services import update_orderitem_quantity, get_or_create_orderitem, get_product, \
    get_or_create_order

logger = logging.getLogger(__name__)


@transaction.atomic
def add_to_cart(request, product_id, quantity):
    """ Main logic of adding product to cart """
    logger.info('inside add_to_cart service')
    order = get_or_create_order(request)
    product = get_product(product_id)
    orderitem = get_or_create_orderitem(product, order, quantity)
    update_orderitem_quantity(orderitem, quantity)


def process_cart(request, id):
    """ This view handles logic of 'add product to cart' button """
    logger.info('inside process_cart view')
    quantity = request.POST.get('quantity', 1)
    try:
        quantity = int(quantity)
    except ValueError:
        return handle_error(request, 'Invalid quantity.')
    try:
        add_to_cart(request, id, quantity)
    except NotEnoughInStock:
        return handle_error(request, 'Not Enough In Stock')
    except Exception as e:
        return handle_error(request, f'An error occurred: {str(e)}')


def handle_error(request, error_message):
    """ Handles error messages """
    messages.error(request, error_message)
    return HttpResponseBadRequest(f'<p class="error">{error_message}.</p>')
