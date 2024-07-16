from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import CustomUser
from .serializers import UserSerializer, ContactSerializer, AddressSerializer


class UserDetailApiView(APIView):
    def get_object(self, pk):
        return get_object_or_404(CustomUser, pk=pk)
    
    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UserSerializer(user)
        
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serailizer.data)
        
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serailizer.data)
        
        return Response(serializer.errors, status=400)


class UserContactApiView(APIView):
    def get(self, request):
        contacts = request.user.contacts.all()
        serializer = ContactSerializer(contacts, many=True)
        
        return Response(serializer.data)
    
    def post(self, request, pk):
        other_user = get_object_or_404(CustomUser, pk=pk)
        serializer = ContactSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(owner=request.user, user=other_user)
            return Response(serializer.data)
        return Response(serailizer.errors, status=400)
 