from django.urls import path

from . import views


urlpatterns = [
    path('', views.auctions, name='auctions'),
    path('auction/<slug:slug>', views.auction, name='auction'),
    path('auction/private/<slug:slug>', views.auction, name='auction-private'),
    path('auction/<slug:slug>/bid/', views.bid, name='auction-bid'),
    
    path('auction/create/', views.auction_create, name='auction-create'),
    path('auction/<slug:slug>/update/', views.auction_update, name='auction-update'),
    path('auction/<slug:slug>/delete/', views.auction_delete, name='auction-delete'),
    
    path('auction/<slug:slug>/like/<user_id>', views.auction_like, name='auction-like'),
    path('auction/<slug:slug>/remind-me/<user_id>', views.remind_me, name='remind-me'),
    
    path('auction/<slug:slug>/comment/add/<user_id>', views.add_comment, name='auction-comment-add'),
    
    path('auction/<slug:slug>/admins/', views.auction_admins, name='auction-admins'),
    path('auction/<slug:slug>/admins/add/', views.auction_admins_add, name='auction-admins-add'),
    path('auction/<slug:slug>/admins/admin/@<username>', views.auction_admin, name='auction-admin'),
    path('auction/<slug:slug>/admins/admin/@<username>/add/', views.auction_admin_add, name='auction-admin-add'),
    path('auction/<slug:slug>/admins/admin/@<username>/delete/', views.auction_admin_delete, name='auction-admin-delete'),
]
