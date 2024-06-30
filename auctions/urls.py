from django.urls import path

from . import views


urlpatterns = [
    path('', views.auctions, name='auctions'),
    path('auction/<slug:slug>', views.auction, name='auction'),
    path('auction/private/<slug:slug>', views.auction_private, name='auction-private'),
    path('auction/<slug:slug>/bid/', views.bid, name='auction-bid'),
    
    path('auction/create/', views.auction_create, name='auction-create'),
    path('auction/<slug:slug>/update/', views.auction_update, name='auction-update'),
    path('auction/<slug:slug>/delete/', views.auction_delete, name='auction-delete'),
    
    path('auction/<slug:slug>/like/<user_id>', views.auction_like, name='auction-like'),
    path('auction/<slug:slug>/view/', views.auction_view, name='auction-view'),
    path('auction/<slug:slug>/remind-me/<user_id>', views.remind_me, name='remind-me'),
]
