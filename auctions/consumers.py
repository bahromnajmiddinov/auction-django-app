from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Auction, ParticipantData, Message


class AuctionBidConsumer(WebsocketConsumer):
    def connect(self):
        self.auction_slug = self.scope['url_route']['kwargs']['slug']
        self.auction = get_object_or_404(Auction, slug=self.auction_slug)
        self.user = self.scope.get('user')
        
        self.accept()

        async_to_sync(self.channel_layer.group_add)(self.auction_slug, self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.auction_slug, self.channel_name)
    
    def receive(self, text_data=None, bytes_data=None):
        loaded_data = json.loads(text_data)
        type = loaded_data['type']
        
        if type == 'message':
            message = Message.objects.create(user=self.user, auction=self.auction, text=loaded_data['message'])
            data = {
                'type': 'chat_message_handler',
                'message_id': message.id,
            }
            
        elif type == 'bid':
            if self.user not in self.auction.participants.all():
                self.auction.participants.add(self.user)
            
            bid = self.auction.participantdata_set.get(participant=self.user, auction=self.auction)
            bid_price = int(loaded_data['price'])
            change_auction_price = False
            if bid_price > bid.price:
                bid.price = bid_price
                bid.save()
                
                if bid_price > self.auction.auction_price and bid_price > self.auction.starter_price:
                    self.auction.auction_price = bid_price
                    self.auction.save()
                    
                    change_auction_price = True
                
            data = {
                'type': 'last_bids_handler',
                'bid_id': bid.id,
                'change_auction_price': change_auction_price,
            }
            
        async_to_sync(self.channel_layer.group_send)(self.auction_slug, data)
    
    def chat_message_handler(self, data):
        message = Message.objects.get(pk=data['message_id'])
        maybe_sender = self.user
        data = {
            'message': render_to_string('auctions/snippets/message.html', {'message': message, 'maybe_sender': maybe_sender}),
            'type': 'message',
        }
        self.send(json.dumps(data))
    
    def last_bids_handler(self, data):
        bid = ParticipantData.objects.get(pk=data['bid_id'])
        last_bid = render_to_string('auctions/snippets/last-bid.html', {'bid': bid})
        data = {
            'last_bid': last_bid,
            'type': 'bid',
            'change_auction_price': data['change_auction_price'],
            'price': bid.price,
        }
        self.send(json.dumps(data))
