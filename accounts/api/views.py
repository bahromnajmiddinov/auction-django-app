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
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    def patch(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
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
        return Response(serializer.errors, status=400)
    

class UserContactsDetailApiView(APIView):
    def get_contact(self, request, user_id):
        other_user = get_object_or_404(id=user_id)
        return get_object_or_404(request.user.contacts, user=other_user)
    
    def get(self, request, user_id):
        user_contact = self.get_contact(request, user_id)
        
        serializer = ContactSerializer(user_contact, many=False)
        
        return Response(serializer.data)
    
    def put(self, request, user_id):
        user_contact = self.get_contact(request, user_id)
        
        serializer = ContactSerializer(user_contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=400)
    
    def delete(self, request, user_id):
        user_contact = self.get_contact(request, user_id)
        
        user_contact.delete()
        
        return Response({'info': 'Contact Deleted.'}, status=204)


class UserAddressApiView(APIView):
    def get(self, request):
        user_addresses = request.user.address_set.all()
        serializer = AddressSerializer(user_addresses, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)


class UserAddressDetailApiView(APIView):
    def get_address(self, request, address_id):
        return get_object_or_404(request.user.address_set, id=address_id)
    
    def get(self, request, address_id):
        user_address = self.get_address(request, address_id)
        serializer = AddressSerializer(user_address, many=False)
        return Response(serializer.data)
    
    def put(self, request, address_id):
        user_address = self.get_address(request, address_id)
        serializer = AddressSerializer(user_address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def patch(self, request, address_id):
        user_address = self.get_address(request, address_id)
        serializer = AddressSerializer(user_address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, address_id):
        user_address = self.get_address(request, address_id)
        user_address.delete()
        return Response({'info': 'Address deleted.'}, status=204)

 