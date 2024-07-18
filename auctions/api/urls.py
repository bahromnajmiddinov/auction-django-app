from django.urls import path

from .views import (
    AuctionListApiView, AuctionDetailApiView, 
    AuctionCommentApiView, auction_like, 
    AuctionAdminApiView, AuctionAdminDetailApiView
)

urlpatterns = [
    path('', AuctionListApiView.as_view(), name='auctions-api'),
    path('auction/<slug:slug>/', AuctionDetailApiView.as_view(), name='auction-api'),
    path('auction/<slug:slug>/like/', auction_like, name='auction-like-api'),
    path('auction/<slug:slug>/comments/', AuctionCommentApiView.as_view(), name='auction-comment-api'),
    path('auction/<slug:auction_slug>/admins/', AuctionAdminApiView.as_view(), name='auctions-admins-api'),
    path('auction/<slug:auction_slug>/admins/admin/<user_id>/', AuctionAdminDetailApiView.as_view(), name='auction-admin-api'),
]


