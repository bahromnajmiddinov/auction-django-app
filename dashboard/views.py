from django.shortcuts import render
from django.db.models import Count

from auctions.models import ParticipantData, Like, Watchers


def dashboard(request):
    auctions = request.user.auctions.all()
    
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
        'all_numbers':  all_numbers,
    }
    
    return render(request, 'dashboard/dashboard.html', context)
    