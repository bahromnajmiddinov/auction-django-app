from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from accounts.api.serializers import UserSerializer
from accounts.models import CustomUser
from auctions.models import Auction, Comment, LocationData, AuctionUserPermission
from auctions.utils import get_client_ip
from .serializersers import AuctionSerializer, CommentSerializer, MessageSerializer, ParticipantDataSerializer, AuctionUserPermissionSerializer
from .permissions import CanEditAuction, CanDeleteAuction, CanAddAdminToAuction


class AuctionListApiView(APIView):
    '''
    API view to handle the listing and creation of auctions.
    '''
    serializer_class = AuctionSerializer
    
    
    @swagger_auto_schema(
        operation_summary="List Auctions",
        operation_description="Retrieves a list of auctions based on the user's authentication status.",
        responses={200: AuctionSerializer(many=True)},
    )
    def get(self, request):
        '''
        Retrieves a list of auctions based on the user's authentication status.

        - If the user is anonymous, only 'PB' type auctions are returned.
        - If the user is authenticated, the returned auctions include:
            * 'PB' type auctions
            * 'PR' Auctions where the user is a watcher
            * 'OC' type auctions where the user is a contact of the owner

        Parameters
        ----------
        request : Request
            The request object containing user information.

        Returns
        -------
        Response
            The response containing serialized auction data.
        '''
        if request.user.is_anonymous:
            auctions = Auction.objects.filter(type='PB')
        else:
            auctions = Auction.objects.filter(Q(type='PB') | Q(user_watchers__in=[request.user]) | (Q(owner__contacts__in=[request.user.id]) & Q(type='OC')))
        serializer = AuctionSerializer(auctions, many=True, context={'request': request})
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Create Auction",
        operation_description="Creates a new auction with the data provided in the request.",
        request_body=AuctionSerializer,
        responses={
            201: AuctionSerializer,
            400: 'Bad Request'
        },
    )
    def post(self, request):
        '''
        Creates a new auction with the data provided in the request.

        - If the data is valid, the auction is saved and returned with a status of 201.
        - If the data is invalid, an error response is returned with a status of 400.

        Parameters
        ----------
        request : Request
            The request object containing auction data.

        Returns
        -------
        Response
            The response containing serialized auction data if successful, or error details if not.
        '''
        serializer = AuctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AuctionDetailApiView(APIView):
    """
    API view to handle retrieving, updating, and deleting an auction by its slug.
    """
    
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    
    def get_permissions(self):
        """
        Get permissions based on the request method.
        
        Returns
        -------
        list
            A list of permission instances.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return [IsAuthenticated(), CanEditAuction()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), CanDeleteAuction()]
        return [IsAuthenticated()]
    
    def get_object(self, slug):
        """
        Retrieve an auction object by its slug.
        
        Parameters
        ----------
        slug : str
            The slug of the auction.
        
        Returns
        -------
        Auction
            The auction object.
        """
        return get_object_or_404(self.queryset, slug=slug)
    
    def get_objects(self, get, queryset, serializer, many=True, context={}):
        """
        Retrieve a serialized list of objects based on the query parameter.
        
        Parameters
        ----------
        get : str
            Query parameter indicating whether to retrieve the objects.
        queryset : QuerySet
            The queryset of objects to retrieve.
        serializer : Serializer
            The serializer class to use.
        many : bool, optional
            Whether to serialize multiple objects (default is True).
        context : dict, optional
            Additional context for the serializer (default is {}).
        
        Returns
        -------
        Serializer
            The serialized objects if 'get' is 'true', otherwise None.
        """
        return serializer(queryset, many=many, context=context) if get == 'true' else None

    @swagger_auto_schema(
        operation_summary="Retrieve Auction",
        operation_description="Retrieve an auction by its slug. Optionally include related messages and bids.",
        manual_parameters=[
            openapi.Parameter('messages', openapi.IN_QUERY, description="Include related messages", type=openapi.TYPE_STRING),
            openapi.Parameter('bids', openapi.IN_QUERY, description="Include related bids", type=openapi.TYPE_STRING),
        ],
        responses={
            200: openapi.Response('Auction data', AuctionSerializer),
            403: 'Forbidden'
        }
    )
    def get(self, request, slug):
        """
        Retrieve an auction by its slug. Optionally include related messages and bids.
        
        Parameters
        ----------
        request : Request
            The request object containing user information.
        slug : str
            The slug of the auction.
        
        Returns
        -------
        Response
            The response containing auction data and optionally related messages and bids.
        """
        get_messages = request.GET.get('messages')
        get_bids = request.GET.get('bids')
        
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
    
    @swagger_auto_schema(
        operation_summary="Update Auction",
        operation_description="Update an auction by its slug.",
        request_body=AuctionSerializer,
        responses={
            200: AuctionSerializer,
            400: 'Bad Request'
        }
    )
    def put(self, request, slug):
        """
        Update an auction by its slug.
        
        Parameters
        ----------
        request : Request
            The request object containing auction data.
        slug : str
            The slug of the auction.
        
        Returns
        -------
        Response
            The response containing updated auction data if successful, or error details if not.
        """
        auction = self.get_object(slug=slug)
        serializer = AuctionSerializer(auction, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    @swagger_auto_schema(
        operation_summary="Partially Update Auction",
        operation_description="Partially update an auction by its slug.",
        request_body=AuctionSerializer,
        responses={
            200: AuctionSerializer,
            400: 'Bad Request'
        }
    )
    def patch(self, request, slug):
        """
        Partially update an auction by its slug.
        
        Parameters
        ----------
        request : Request
            The request object containing auction data.
        slug : str
            The slug of the auction.
        
        Returns
        -------
        Response
            The response containing updated auction data if successful, or error details if not.
        """
        auction = self.get_object(slug=slug)
        serializer = AuctionSerializer(auction, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    @swagger_auto_schema(
        operation_summary="Delete Auction",
        operation_description="Delete an auction by its slug.",
        responses={
            204: 'No Content',
        }
    )
    def delete(self, request, slug):
        """
        Delete an auction by its slug.
        
        Parameters
        ----------
        request : Request
            The request object.
        slug : str
            The slug of the auction.
        
        Returns
        -------
        Response
            A response with status 204 if the deletion is successful.
        """
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


class AuctionAdminApiView(APIView):
    queryset = Auction.objects.all()
    permission_classes = [CanAddAdminToAuction(), IsAuthenticated()]
    
    def get(self, request):
        auctions = self.get_queryset()
        
        if request.user in auctions.permissions.all():
            serializer = UserSerializer(auctions.permissions.all(), many=True)
            return Response(serializer.data)
        
        return Response({'error': 'You do not have permission to access this resource.'}, status=403)
    
    def post(self, request):
        slug = request.data.get('auctionSlug')
        user_id = request.data.get('userId')
        
        auction = get_object_or_404(Auction, slug=slug)
        other_user = get_object_or_404(CustomUser, id=user_id)
        
        if other_user not in auction.permissions.all():
            auction.permissions.add(other_user)
            return Response({'message': 'User added to permissions.'}, status=200)
        
        return Response({'info': 'User already admin.'}, status=200)


class AuctionAdminDetailApiView(APIView):
    queryset = AuctionUserPermission.objects.all()
    permission_classes = [CanAddAdminToAuction(), IsAuthenticated()]
    
    def get(self, request, auction_slug, user_id):
        auction = get_object_or_404(Auction, slug=auction_slug)
        user = get_object_or_404(CustomUser, id=user_id)
        
        permission = auction.auctionuserpermission_set.filter(user=user).first()
        
        if permission:
            serializer = AuctionUserPermissionSerializer(permission)
            return Response(serializer.data)
        
        return Response({'error': 'Permission not found.'}, status=404)
    
    def put(self, request, auction_slug, user_id):
        auction = get_object_or_404(Auction, slug=auction_slug)
        user = get_object_or_404(CustomUser, id=user_id)
        
        permission = auction.auctionuserpermission_set.filter(user=user).first()
        
        if permission:
            serializer = AuctionUserPermissionSerializer(permission, data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        
        return Response({'error': 'Permission not found.'}, status=404)
    
    def delete(self, request, auction_slug, user_id):
        auction = get_object_or_404(Auction, slug=auction_slug)
        user = get_object_or_404(CustomUser, id=user_id)
        
        permission = auction.auctionuserpermission_set.filter(user=user).first()
        
        if permission:
            permission.delete()
            return Response({'message': 'Permission deleted.'}, status=204)
        
        return Response({'error': 'Permission not found.'}, status=404)
    

