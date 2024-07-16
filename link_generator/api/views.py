# TODO: write custom permisison

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from link_generator.models import Link
from .serializers import LinkSerializer
from auctions.models import Auction
from auctions.api.serializersers import AuctionSerializer


class PrivateLinkListApiView(APIView):
    def get(self, request, slug):
        auction = get_object_or_404(Auction, slug=slug, type='PR')
        
        if request.user not in auction.permissions.all():
            return Response('You are not allowed!', status=403)
        
        all_private_links = auction.link_set.all()
        
        return Response({'allPrivateLinks': LinkSerializer(all_private_links, many=True), 'auction': AuctionSerializer(auction, many=False)})
    
    def post(self, request, slug):
        auction = get_object_or_404(Auction, slug=slug)
    
        if request.user not in auction.permissions.all():
            return Response('You are not allowed!', status=403)
        
        serializer = LinkSerializer(data=request.data)
        
        if serializer.is_valid():
            link = serializer.save(commit=False)
            link.auction = auction
            link.save()
            link.users.add(request.user)
            
            return Response(serializer.data)
        
        return Response(serializer.errors, staus=400)


class PrivateLinkDetailApiView(APIView):
    def get(self, request, path):
        link = get_object_or_404(Link, path=path)
        if not link.is_expired():
            return Response('Link expired', status=404)
        
        link.auction.user_watchers.add(request.user)
        
        if request.user not in link.users.all():
            link.users.add(request.user)
        
        return Response('auction-private', link.auction.slug)
    
    def delete(self, request, path):
        link = get_object_or_404(Link, path=path)
    
        if request.user in link.auction.permissions.all():
            link.delete()
            return Response('deleted')
        
        return Response('You are not allowed!', status=403)
