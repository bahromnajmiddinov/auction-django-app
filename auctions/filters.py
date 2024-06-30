import django_filters

from .models import Auction


class AuctionFilter(django_filters.FilterSet):
    description = django_filters.CharFilter(lookup_expr='icontains')
    
    starter_price = django_filters.NumberFilter()
    starter_price__gt = django_filters.NumberFilter(field_name='starter_price', lookup_expr='gt')
    starter_price__lt = django_filters.NumberFilter(field_name='starter_price', lookup_expr='lt')
    auction_price = django_filters.NumberFilter()
    auction_price__gt = django_filters.NumberFilter(field_name='auction_price', lookup_expr='gt')
    auction_price__lt = django_filters.NumberFilter(field_name='auction_price', lookup_expr='lt')
    
    class Meta:
        model = Auction
        fields = ['title', 'description', 'start_time', 'end_time', 'starter_price', 'starter_price', 'participants', 'user_watchers', 'user_likes', 'created']
