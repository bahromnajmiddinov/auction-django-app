from rest_framework import serializers

from auctions.models import Auction, Comment, Message, ParticipantData
from labeler.api.serializers import TagSerializer, CategorySerializer


class AuctionSerializer(serializers.ModelSerializer):
    current_price = serializers.SerializerMethodField('get_current_price')
    tags = TagSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Auction
        fields = '__all__'
        read_only_fields = ['auction_price', 'winner', 'owner']
    
    def get_current_price(self, instance):
        return instance.get_current_price


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='user-detail-api')
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'auction']


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='user-detail-api')
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['auction']


class ParticipantDataSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ParticipantData
        fields = '__all__'
        read_only_fields = ['auction', 'participant']
        
