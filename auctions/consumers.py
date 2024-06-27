from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class AuctionBidConsumer(WebsocketConsumer):
    def connect(self):
        pass
    
    def disconnect(self, close_code):
        pass
    
    def receive(self, text_data=None, bytes_data=None):
        pass
    
    
