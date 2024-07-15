from config import settings
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from celery import shared_task

from auctions.models import Auction


@shared_task(bind=True)
def time_end(self, auction_id, task):
    auction = get_object_or_404(Auction, pk=auction_id)
    participants = auction.participants.all()
    
    context = {
        'auction_title': auction.title,
        'auction_summary': auction.summary,
        'auction_slug': auction.slug,
    }
    
    if task == 'start_time':
        email_title = f'Auction Started: {auction.title}'
        template_name = 'auctions/email/start_email_template.html'
        context['sarting_bid'] = auction.starter_price
    elif task == 'end_time':
        email_title = f'Auction Ended: {auction.title}'
        template_name = 'auctions/email/end_email_template.html'
        context['winning_bid'] = auction.get_current_price
        
        html_message_winner = render_to_string('auctions/email/auction_winner_template.html', {
            'winner_name': auction.winner.first_name,
            'item_name': auction.title,
            'winner_email': auction.winner.email,
            'winner_phone': auction.winner.phone,
            'auction_end_date': auction.end_time,
        })
        plain_message_winner = strip_tags(html_message)
        
        send_mail(
            subject='You WIN!',
            plain_message=plain_message_winner,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[auction.winner.email],
            html_message=html_message_winner,
            fail_silently=True,
        )
    
    
    for participant in participants:
        context['full_name'] = participant.get_full_name()
        
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=email_title,
            plain_message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[participant.email],
            html_message=html_message,
            fail_silently=True,
        )
    
