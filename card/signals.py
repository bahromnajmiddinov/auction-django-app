from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from auctions.models import Auction
from .models import Card, CardItem


@receiver(user_logged_in)
def move_session_data_to_database(sender, request, user, **kwargs):
    # Get session data
    cart = request.session.get('cart', [])

    # Iterate through the session data and save to database
    for product_id in cart:
        # Retrieve product details
        product = Auction.objects.get(id=product_id)

        # Create a new CartItem object linked to the logged-in user
        cart, created = Card.objects.get_or_create(user=user)
        CardItem.objects.create(auction=product, card=cart)

    # Clear the session after transferring data to database
    if cart:
        del request.session['cart']

