from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from auctions.models import Auction, Like, ParticipantData, Watchers
from auctions.api.serializersers import AuctionSerializer
from auctions.api.permissions import IsAdminOfAuction


@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
    
    data = {
        'auctions': AuctionSerializer(auctions, many=True),
        'admin_of_auctions': AuctionSerializer(admin_of_auctions, many=True),
        'all_numbers':  all_numbers,
    }
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOfAuction])
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
    
    data = {
        'auction': AuctionSerializer(auction, many=False),
        'user_counts_by_country': user_counts_by_country,
        'all_numbers': all_numbers,
    }
    return Response(data)
