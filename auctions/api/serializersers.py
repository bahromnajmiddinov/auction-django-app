from rest_framework import serializers

from auctions.models import (Auction, Comment, 
                             Message, ParticipantData, 
                             AuctionUserPermission, ImageField, 
                             VideoField, AdditionalField)
from labeler.api.serializers import TagSerializer, CategorySerializer


class ImageFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageField
        fields = '__all__'
        

class VideoFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoField
        fields = '__all__'


class AdditionalFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalField
        fields = '__all__'
        
        
class AuctionSerializer(serializers.ModelSerializer):
    current_price = serializers.SerializerMethodField('get_current_price')
    tags = TagSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    image_fields = ImageFieldSerializer(many=True, required=False)
    video_fields = VideoFieldSerializer(many=True, required=False)
    additional_fields = AdditionalFieldSerializer(many=True, required=False)
    
    class Meta:
        model = Auction
        fields = '__all__'
        read_only_fields = ['auction_price', 'winner', 'owner']
    
    def get_current_price(self, instance):
        return instance.get_current_price
    
    def create(self, validated_data):
        images_data = validated_data.pop('image_fields', [])
        videos_data = validated_data.pop('video_fields', [])
        additionals_data = validated_data.pop('additional_fields', [])
        
        auction = Auction.objects.create(**validated_data)
        for image_data in images_data:
            ImageField.objects.create(auction=auction, **image_data)
        
        for video_data in videos_data:
            VideoField.objects.create(auction=auction, **video_data)
        
        for additional_data in additionals_data:
            AdditionalField.objects.create(auction=auction, **additional_data)
        
        return auction


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
        

class AuctionUserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionUserPermission
        fields = '__all__'
        
