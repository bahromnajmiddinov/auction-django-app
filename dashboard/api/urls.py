from django.urls import path

from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard-api'),
    path('', views.dashboard_auction_detail, name='dashboard-auction-detail-api'),
]

