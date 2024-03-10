from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from shopping.models import Review, Product
from shopping.services.order_services import get_product


@login_required
def add_review(request, id):
    """ This service is for adding review to the product """
    product = get_product(id)
    rating = request.POST.get('rating')
    text = request.POST.get('text')

    # Check if the user has already left a review for this product
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    if existing_review is not None:
        # If a review exists, update it
        existing_review.rating = rating
        existing_review.text = text
        existing_review.save()
    else:
        # If no review exists, create a new one
        Review.objects.create(product=product, user=request.user, rating=rating, text=text)


def get_reviews_by_product(id):
    """ This service is checking if product exists then getting reviews of this product """
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product)
    return product, reviews


def get_review_by_user(request, id):
    """ This service is checking if product exists then getting reviews of this product by user """
    product = get_product(id)
    existing_review = Review.objects.filter(product=product, user=request.user).first()
    return product, existing_review
