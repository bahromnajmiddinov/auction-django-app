from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view

from order.models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from accounts.api.serializers import AddressSerializer
from card.api.serializers import CartItemSerializer


@api_view(['GET'])
def checkout(request):
    saved_addresses = request.user.address_set.all()
    card_items = request.user.cards.last().items.all()
    
    if not card_item.exists():
        return Response({'info': 'cart cannot be empty'}, status=405)
    
    total_count = 0
    total_price = 0
    for card_item in card_items:
        auction = card_item.auction
        # check user if the winner of the auction
        if auction.winner != request.user or auction.orderitem_set.exists():
            return Response('You are winner or already ordered item!', status=403)
            
        total_price += auction.get_current_price
        total_count += 1
    
    all_numbers = {
        'total_items': total_count,
        'total_price': total_price,
    }
    
    data = {
        'savedAddresses': AddressSerializer(saved_addresses, many=True).data,
        'card_items': CartItemSerializer(card_items, many=True).data,
        'all_numbers': all_numbers,
    }
    
    return Response(data)


@api_view(['GET'])
def order_data(request, order_id=None):
    user = request.user
    
    # get order data
    if order_id:
        order = get_object_or_404(user.order_set, pk=order_id)
    # create new order
    else:
        card_items = user.cards.last().items.all()
        
        payment_method = request.GET.get('payment-radio', None)
        address_id = request.GET.get('address-radio', None)
        
        if payment_method is None:
            return Response('Payment method is required!', status=400)
        
        if address_id is None:
            return Response('Address is required!', status=400)
        
        address = get_object_or_404(user.address_set, pk=address_id)
        
        total_price = 0
        order = Order.objects.create(user=user, payment_method=payment_method, address=address, total_amount=0)
        for card_item in card_items:
            OrderItem.objects.create(order=order, product=card_item.auction, price=card_item.auction.get_current_price)
            total_price += card_item.auction.get_current_price
            card_item.delete()
        
        order.total_amount = total_price
        order.save()
    
    data = {
        'order': OrderSerializer(order, many=False),
        'order_items': OrderItemSerializer(order.orderitem_set.all(), many=True),
    }
        
    return Response(data)
