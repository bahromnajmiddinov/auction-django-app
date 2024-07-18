from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from auctions.models import Auction
from card.models import Card, CardItem
from .serializers import CartItemSerializer


class CartDetailApiView(APIView):
    def get(self, request):
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
        
        data = {
            'cartItems': CartItemSerializer(cart_items, many=True, context={'request': request}),
            'totalItems': total_count,
            'totalPrice': total_price,
        }

        return Response(data)


class AddToCartApiView(APIView):
    def get(self, request, slug):
        auction = get_object_or_404(Auction, slug=slug)
        data = {
            'saved': False
        }
        
        # If user not authenticated, cartItems will be saved to sessions!
        if request.user.is_anonymous:
            cart = request.session.get('cart', [])
            if not str(auction.id) in cart:
                if not auction.orderitem_set.exists():
                    cart.append(str(auction.id))
                    data['saved'] = True
                else:
                    return Response('Item already ordered!', status=403)
            else:
                cart.remove(str(auction.id))
                
            request.session['cart'] = cart
            
            return Response(data)
        
        # Authenticated users cartItems will be saved to database!
        user = request.user
        
        card, created = Card.objects.get_or_create(user=user)
        if not auction.orderitem_set.exists():
            card_item, created = CardItem.objects.get_or_create(card=card, auction=auction)
            data['saved'] = True
        else:
            return Response('Item already ordered!', status=403)
        
        if not created:
            card_item.delete()
            data['saved'] = False
        
        return Response(data)
    

@api_view(['GET'])
def is_item_saved(request, auction_slug):
    auction = get_object_or_404(Auction, slug=auction_slug)
    
    if request.user.is_anonymous:
        saved = True if str(auction.id) in request.session.get('cart', []) else False
    else:
        saved = True if request.user.cards.first().items.filter(auction=auction).exists() else False
    
    return Response({'saved': saved})
        