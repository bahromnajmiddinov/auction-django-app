from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from celery import shared_task

from auctions.models import Auction


@shared_task(bind=True)
def time_end(self, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    participants = auction.participants.all()
    
    for participant in participants:
        send_mail(
            'Auction End',
            f'Auction {auction.title} has ended',
            'Auction End',
            [participant.email],
            fail_silently=False,
        )
