from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from accounts.models import CustomUser
from auctions.models import Auction
from .models import Card, CardItem


def card_detail(request):
    pass


def add_to_card(request, slug, user_id):
    auction = get_object_or_404(Auction, slug=slug)
    user = get_object_or_404(CustomUser, pk=user_id)
    
    data = {'success': None}
    
    card, created = Card.objects.get_or_create(user=user)
    card_item, created = CardItem.objects.get_or_create(card=card, auction=auction)
    
    data['success'] = True
    
    return JsonResponse(data)


def remove_from_card(request):
    pass


def delete_from_card(request):
    pass
