from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from auctions.models import Auction, Comment, LocationData
from auctions.utils import get_client_ip
from .serializersers import AuctionSerializer, CommentSerializer, MessageSerializer, ParticipantDataSerializer
from .permissions import CanEditAuction, CanDeleteAuction, CanAddAdminToAuction


class AuctionListApiView(APIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    
    def get(self, request):
        auctions = Auction.objects.all()
        serializer = AuctionSerializer(auctions, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AuctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AuctionDetailApiView(APIView):
    '''
    Auction Api
    Bid api view
    '''
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return [IsAuthenticated(), CanEditAuction()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), CanDeleteAuction()]
        return [IsAuthenticated()]
    
    def get_object(self, slug):
        return get_object_or_404(self.queryset, slug=slug)
    
    def get_objects(self, get, queryset, serializer, many=True, context={}):
        return serializer(queryset, many=many, context=context) if get == 'true' else None

    def get(self, request, slug):
        get_messages = request.GET.get('messages')
        get_bids = request.GET.get('bids')
        get_tags = request.GET.get('tags')
        get_categories = request.GET.get('categories')
        
        auction = self.get_object(slug=slug)
        
        chat_message_serializer = self.get_objects(get_messages, auction.messages.all(), MessageSerializer)
        bids_serializer = self.get_objects(get_bids, auction.participantdata_set.all(), ParticipantDataSerializer)
        
        if request.user not in auction.user_watchers.all():
            if auction.type != 'PB':
                return Response('You are not allowed!', status=403)
            if not request.user.is_anonymous:
                auction.user_watchers.add(request.user)
        
        client_ip = get_client_ip(request)
        if client_ip.country is not None:
            client_country = client_ip.country
            client_city = client_ip.city
            ip_address = client_ip.ip
            LocationData.objects.get_or_create(auction=auction, country=client_country, city=client_city, ip_address=ip_address)
        
        serializer = AuctionSerializer(auction, context={'request': request})
        
        data = {
            'auction': serializer.data,
        }
        
        if chat_message_serializer:
            data['chatMessages'] = chat_message_serializer.data
        
        if bids_serializer:
            data['bids'] = bids_serializer.data
        
        return Response(data)
    
    def put(self, request, slug):
        auction = self.get_object(slug=slug)
        serializer = AuctionSerializer(auction, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    def patch(self, request, slug):
        auction = self.get_object(slug=slug)
        serializer = AuctionSerializer(auction, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    def delete(self, request, slug):
        auction = self.get_object(slug=slug)
        auction.delete()
        return Response(status=204)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def auction_like(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    liked = None
    if request.user in auction.user_likes.all():
        auction.user_likes.remove(request.user)
        liked = False
    else:
        auction.user_likes.add(request.user)
        liked = True
    
    return Response({'liked': liked})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def auction_remaind_me(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    remainded = None
    if request.user in auction.participants.all():
        auction.participants.remove(request.user)
        remainded = False
    else:
        auction.participants.add(request.user)
        remainded = True
    
    return Response({'remainded': remainded})


class AuctionCommentApiView(APIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get(self, request, slug):
        auction = get_object_or_404(Auction, slug=slug)
        comments = auction.comments.all()
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, slug):
        auction = get_object_or_404(Auction, slug=slug)
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user, auction=auction)
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)

