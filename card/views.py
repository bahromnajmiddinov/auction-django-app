from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from accounts.models import CustomUser
from auctions.models import Auction
from .models import Card, CardItem


def card_detail(request):
    total_count = 0
    total_price = 0
    
    if request.user.is_anonymous:
        cart = request.session.get('cart', [])
        cart_items = []
        for auction in Auction.objects.filter(id__in=cart):
            cart_items.append({'auction': auction})
            total_price += auction.get_current_price
            total_count += 1
    else:
        card = request.user.cards.last()
        cart_items = card.items.all()
    
        for auction_price in cart_items:
            total_price += auction_price.auction.get_current_price
            total_count += 1
    
    all_numbers = {
        'total_items': total_count,
        'total_price': total_price,
    }
    
    return render(request, 'card/card.html', {'card_items': cart_items, 'all_numbers': all_numbers})


def add_to_card(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    
    if request.user.is_anonymous:
        cart = request.session.get('cart', [])
        if not str(auction.id) in cart:
            if not auction.orderitem_set.exists():
                cart.append(str(auction.id))
            else:
                return ('auction', auction.slug)
        else:
            cart.remove(str(auction.id))
            
        request.session['cart'] = cart
        
        return redirect('auction', auction.slug)
        
    user = request.user
    
    card, created = Card.objects.get_or_create(user=user)
    if not auction.orderitem_set.exists():
        card_item, created = CardItem.objects.get_or_create(card=card, auction=auction)
    else:
        return redirect('auction', auction.slug)
    
    if not created:
        card_item.delete()
    
    return redirect('auction', auction.slug)
