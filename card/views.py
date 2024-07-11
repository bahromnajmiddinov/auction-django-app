from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from accounts.models import CustomUser
from auctions.models import Auction
from .models import Card, CardItem


def card_detail(request):
    card = request.user.cards.last()
    card_items = card.items.all()
    
    total_count = 0
    total_price = 0
    for auction_price in card_items:
        total_price += auction_price.auction.get_current_price
        total_count += 1
    
    all_numbers = {
        'total_items': total_count,
        'total_price': total_price,
    }
    
    return render(request, 'card/card.html', {'card_items': card_items, 'all_numbers': all_numbers})


def add_to_card(request, slug):
    if request.user.is_anonymous:
        pass
        
    auction = get_object_or_404(Auction, slug=slug)
    user = request.user
    
    data = {'added': False}
    
    card, created = Card.objects.get_or_create(user=user)
    card_item, created = CardItem.objects.get_or_create(card=card, auction=auction)
    
    if created:
        data['added'] = True
    else:
        card_item.delete()
    
    return JsonResponse(data)


def remove_from_card(request):
    pass
