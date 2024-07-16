from rest_framework import serializers

from auctions.models import Auction, Comment, Message, ParticipantData


class AuctionSerializer(serializers.ModelSerializer):
    current_price = serializers.SerializerMethodField('get_current_price')
    
    class Meta:
        model = Auction
        fields = '__all__'
    
    def get_current_price(self, instance):
        return instance.get_current_price


class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='')
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'auction']


class MessageSerializer(serializers.ModelSerializer):
    # sender = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='user-detail')
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'auction']


class ParticipantDataSerializer(serializers.ModelSerializer):
    class Meta: 
        model = ParticipantData
        fields = '__all__'
        read_only_fields = ['auction', 'participant']
