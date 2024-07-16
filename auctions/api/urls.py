from django.urls import path

from .views import AuctionListApiView, AuctionDetailApiView, AuctionCommentApiView, auction_like


urlpatterns = [
    path('', AuctionListApiView.as_view(), name='auctions-api'),
    path('auction/<slug:slug>/', AuctionDetailApiView.as_view(), name='auction-api'),
    path('auction/<slug:slug>/like/', auction_like, name='auction-like-api'),
    path('auction/<slug:slug>/comments/', AuctionCommentApiView.as_view(), name='auction-comment-api'),
]


