from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from accounts.forms import AddressForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    saved_addresses = request.user.address_set.all()
    new_address = AddressForm()
    card_items = request.user.cards.last().items.all()
    
    total_count = 0
    total_price = 0
    for card_item in card_items:
        auction = card_item.auction
        # check user if the winner of the auction
        if auction.winner != request.user and auction.orderitem_set.exits():
            return HttpResponse('you cant')
            
        total_price += auction.get_current_price
        total_count += 1
    
    all_numbers = {
        'total_items': total_count,
        'total_price': total_price,
    }
    
    context = {
        'saved_addresses': saved_addresses,
        'new_address': new_address,
        'card_items': card_items,
        'all_numbers': all_numbers,
    }
    
    return render(request, 'order/checkout.html', context)


@login_required
def order_data(request, order_id=None):
    user = request.user
    
    # get order data
    if order_data:
        order = get_object_or_404(user.order_set, pk=order_id)
    # create new order
    else:
        card_items = user.cards.last().items.all()
        
        payment_method = request.POST.get('payment-radio')
        
        address_id = request.POST.get('address-radio')
        
        if address_id == 'new_address':
            new_address = AddressForm(request.POST)
            if new_address.is_valid():
                address = new_address.save(commit=False)
                address.user = user
                address.save()
            else:
                return render(request, 'order/checkout.html', {'new_address': new_address})
        else:
            address = get_object_or_404(user.address_set, pk=address_id)
        
        total_price = 0
        order = Order.objects.create(user=user, payment_method=payment_method, address=address, total_amount=0)
        for card_item in card_items:
            OrderItem.objects.create(order=order, product=card_item.auction, price=card_item.auction.get_current_price)
            total_price += card_item.auction.get_current_price
            card_item.delete()
        
        order.total_amount = total_price
        order.save()
    
    context = {
        'order': order,
        'order_items': order.orderitem_set.all(),
    }
        
    return render(request, 'order/order-data.html', context)
