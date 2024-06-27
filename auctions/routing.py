from django.urls import path

from . import consumers


ASGI_urlpatterns = [
    path('websocket/auction-bid/<slug:slug', consumers.AuctionBidConsumer),
]
