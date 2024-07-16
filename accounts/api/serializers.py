from rest_framework import serializers

from accounts.models import CustomUser, Contact, Address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'avatar', 'username', 'email', 'first_name', 'last_name', 'description', 'type']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['user', 'first_name', 'last_name']
        

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
