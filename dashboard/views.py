from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from auctions.models import Auction, ParticipantData, Like, Watchers, LocationData


def dashboard(request):
    auctions = request.user.auctions.all()
    admin_of_auctions = request.user.auctionuserpermission_set.exclude(auction__owner=request.user)
    
    auctions_ids = auctions.values_list('id', flat=True)
    
    total_likes = Like.objects.filter(auction__id__in=auctions_ids).count()
    total_users = ParticipantData.objects.filter(auction__id__in=auctions_ids).count()
    total_views = Watchers.objects.filter(auction__id__in=auctions_ids).count()
    
    all_numbers = {
        'total_auctions': auctions.count(),
        'total_users': total_users,
        'total_likes': total_likes,
        'total_views': total_views,
    }
    
    context = {
        'auctions': auctions,
        'admin_of_auctions': admin_of_auctions,
        'all_numbers':  all_numbers,
    }
    
    return render(request, 'dashboard/dashboard.html', context)


def dashboard_auction_detail(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    locations = auction.users_locations.all()
    
    user_counts_by_country = locations.values('country').annotate(user_count=Count('ip_address'))
    total_users = auction.participants.count()
    total_likes = auction.user_likes.count()
    total_views = auction.user_watchers.count()
    
    all_numbers = {
        'total_users': total_users,
        'total_likes': total_likes,
        'total_views': total_views,
    }
    
    context = {
        'auction': auction,
        'user_counts_by_country': user_counts_by_country,
        'all_numbers': all_numbers,
    }
    return render(request, 'dashboard/dashboard-detail.html', context)
    