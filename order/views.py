from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from accounts.forms import AddressForm


@login_required
def checkout(request):
    saved_addresses = request.user.address_set.all()
    new_address = AddressForm()
    card_items = request.user.cards.last().items.all()
    
    total_count = 0
    total_price = 0
    for auction_price in card_items:
        # check user if the winner of the auction
        if auction_price.auction.winner != request.user:
            return HttpResponse('you cant')
            
        total_price += auction_price.auction.get_current_price
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
def order_data(request):
    return render(request, 'order/order-data.html')
