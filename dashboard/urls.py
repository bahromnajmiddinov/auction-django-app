from django.urls import path

from . import views


urlpatterns = [
    path('main/', views.dashboard, name='dashboard'),
    path('auction/<slug>', views.dashboard_auction_detail, name='dashboard-auction-detail'),
]
