from django.shortcuts import render, get_object_or_404

from auctions.models import Auction
from .models import Card, CardItem


def card_detail(request):
    pass


def add_to_card(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    
    card, created = Card.objects.get_or_create(user=request.user)
    card_item, created = CardItem.objects.get_or_create(card=card, auction=auction)
    
    return render('auction', slug)


def remove_from_card(request):
    pass


def delete_from_card(request):
    pass
