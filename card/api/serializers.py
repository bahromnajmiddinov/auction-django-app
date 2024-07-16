from rest_framework import serializers

from card.models import CardItem


class CartItemSerializer(serializers.ModelSerializer):
    auction = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='auction-api')
    
    class Meta:
        model = CardItem
        fields = '__all__'
