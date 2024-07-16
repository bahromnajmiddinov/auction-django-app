from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from auctions.models import Auction, Comment
from .serializersers import AuctionSerializer, CommentSerializer, MessageSerializer, ParticipantDataSerializer


class AuctionListApiView(APIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    
    def get(self, request):
        auctions = Auction.objects.all()
        serializer = AuctionSerializer(auctions, many=True)
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
    
    def get_object(self, slug):
        return get_object_or_404(self.queryset, slug=slug)

    def get(self, request, slug):
        get_messages = request.GET.get('messages')
        get_bids = request.GET.get('bids')
        
        auction = self.get_object(slug=slug)
        
        chat_message_serializer = None
        bids_serializer = None
        
        if get_messages == 'true':
            chat_messages = auction.messages.all()
            chat_message_serializer = MessageSerializer(chat_messages, many=True, context={'request': request})
        
        if get_bids == 'true':
            bids = auction.participantdata_set.all()
            bids_serializer = ParticipantDataSerializer(bids, many=True)
        
        serializer = AuctionSerializer(auction)
        
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

