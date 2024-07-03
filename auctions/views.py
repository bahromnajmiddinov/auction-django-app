#TODO: add pagination
#TODO: after auction end users cannot add new prices
from django.shortcuts import render, redirect, get_object_or_404
# from django.pagination import paginator
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.http import Http404, JsonResponse

import json
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django_filters.views import FilterView

from .utils import get_client_ip, code_to_country_name
from .models import Auction, ImageField, VideoField, AdditionalField, AuctionUserPermission, ParticipantData, LocationData, Comment
from .forms import AuctionForm, ImageFieldForm, VideoFieldForm, AdditionalFieldForm, AuctionUserPermissionForm
from accounts.models import CustomUser
from .filters import AuctionFilter


def _time_scheduler(date_obj, schedule_name, auction_id):
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    hour = date_obj.hour
    minute = date_obj.minute 
    
    schedule, created = CrontabSchedule.get_or_create(year=year, month=month, day=day, hour=hour, minute=minute)
    task = PeriodicTask.objects.create(crontab=schedule, name=schedule_name, task='tasks.time_end', args=json.dumps((auction_id,)))


def auctions(request):
    all_auctions = Auction.objects.filter(Q(type='PB') | Q(user_watchers__in=[request.user]) | (Q(owner__in=CustomUser.objects.filter(contacts__user=request.user)) & Q(type='OC')))
    
    context = {
        'all_auctions': all_auctions,
    }
    
    return render(request, 'auctions/auctions.html', context)


def auction(request, slug):
    auction_detail = get_object_or_404(Auction, slug=slug, type='PB')
    
    client_ip = get_client_ip(request)
    if client_ip.country is not None:
        client_country = client_ip.country
        client_city = client_ip.city
        ip_address = client_ip.ip
        LocationData.objects.get_or_create(auction=auction_detail, country=client_country, city=client_city, ip_address=ip_address)
    
    if request.user not in auction_detail.participants.all():
        auction_detail.user_watchers.add(request.user)
        
    context = {
        'auction': auction_detail,
    }
        
    return render(request, 'auctions/auction-detail.html', context)


def auction_private(request, slug):
    auction_detail = get_object_or_404(Auction, slug=slug)
    
    client_ip = get_client_ip(request)
    if client_ip.country is not None:
        client_country = client_ip.country
        client_city = client_ip.city
        ip_address = client_ip.ip
        LocationData.objects.get_or_create(auction=auction_detail, country=client_country, city=client_city, ip_address=ip_address)
    
    if not request.user in auction_detail.user_watchers.all():
        return Http404()
    
    context = {
        'auction': auction_detail
    }
    
    return render(request, 'auctions/auction-detail.html', context)


def bid(request, slug):
    auction_detail = get_object_or_404(Auction, slug=slug)
    auction_message = auction_detail.messages.all()
    bids = auction_detail.participantdata_set.all()
    
    context = {
        'auction': auction_detail,
        'auction_message': auction_message,
        'bids': bids,
    }
    
    return render(request, 'auctions/bid.html', context)


def auction_create(request):
    auction_form = AuctionForm()
    
    ImageFieldFormset = inlineformset_factory(Auction, ImageField, form=ImageFieldForm, extra=0, fields=('image',))
    image_formset = ImageFieldFormset()
    
    VideoFieldFormset = inlineformset_factory(Auction, VideoField, form=VideoFieldForm, extra=0, fields=('video',))
    video_formset = VideoFieldFormset()
    
    AdditionalFieldFormset = inlineformset_factory(Auction, AdditionalField, form=AdditionalFieldForm, extra=1)
    additional_formset = AdditionalFieldFormset()
    
    if request.method == 'POST':
        auction_form = AuctionForm(request.POST, request.FILES)
        image_formset = ImageFieldFormset(request.POST, request.FILES)
        video_formset = VideoFieldFormset(request.POST, request.FILES)
        additional_formset = AdditionalFieldFormset(request.POST, request.FILES)
        print([auction_form.is_valid(), image_formset.is_valid(), video_formset.is_valid(), additional_formset.is_valid()])
        if all([auction_form.is_valid(), image_formset.is_valid(), video_formset.is_valid(), additional_formset.is_valid()]):
            new_auction = auction_form.save(commit=False)
            new_auction.owner = request.user
            new_auction.save()
            new_auction.permissions.add(request.user)
            user_permission = AuctionUserPermission.objects.get(user=request.user, auction=new_auction)
            user_permission.can_edit = True
            user_permission.can_delete = True
            user_permission.can_add_admin = True
            user_permission.save()
            
            for image_form in image_formset:
                new_image_form = image_form.save(commit=False)
                new_image_form.auction = new_auction
                new_image_form.save()
            
            for video_form in video_formset:
                new_video_form = video_form.save(commit=False)
                new_video_form.auction = new_auction
                new_video_form.save()
            
            for additional_form in additional_formset:
                new_additional_form = additional_form.save(commit=False)
                new_additional_form.auction = new_auction
                new_additional_form.save()
            
            if new_auction.start_time:
                pass
            
            if new_auction.end_time:
                pass
            
            return redirect('auction', new_auction.slug)
        
    context = {
        'auction_form': auction_form,
        'image_formset': image_formset,
        'video_formset': video_formset,
        'additional_formset': additional_formset,
    }
    
    return render(request, 'auctions/auction-create-update.html', context)


def auction_update(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    can_user_edit = get_object_or_404(AuctionUserPermission, user=request.user, auction=auction).can_edit
    if can_user_edit:
        auction_form = AuctionForm(instance=auction)
        ImageFieldFormset = inlineformset_factory(Auction, ImageField, form=ImageFieldForm, extra=0, fields=('image',))
        image_formset = ImageFieldFormset(instance=auction)
        
        VideoFieldFormset = inlineformset_factory(Auction, VideoField, form=VideoFieldForm, extra=0, fields=('video',))
        video_formset = VideoFieldFormset(instance=auction)
        
        AdditionalFieldFormset = inlineformset_factory(Auction, AdditionalField, form=AdditionalFieldForm, extra=0)
        additional_formset = AdditionalFieldFormset(instance=auction)
        
        if request.method == 'POST':
            auction_form = AuctionForm(request.POST, request.FILES, instance=auction)
            image_formset = ImageFieldFormset(request.POST, request.FILES, queryset=auction)
            video_formset = VideoFieldFormset(request.POST, request.FILES, queryset=auction)
            additional_formset = AdditionalFieldFormset(request.POST, request.FILES, queryset=auction)
            
            if all([auction_form.is_valid(), image_formset.is_valid(), video_formset.is_valid(), additional_formset.is_valid()]):
                auction_form.save()
                for image_form in image_formset:
                    image_form.save()
                
                for video_form in video_formset:
                    video_form.save()
                
                for additional_form in additional_formset:
                    additional_form.save()
                
                return redirect('auction', auction.slug)
            
        context = {
            'auction_form': auction_form,
            'image_formset': image_formset,
            'video_formset': video_formset,
            'additional_formset': additional_formset,
            'auction': auction,
        }
        
        return render(request, 'auctions/auction-create-update.html', context)


def auction_delete(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    can_user_delete = get_object_or_404(AuctionUserPermission, user=request.user, auction=auction).can_delete
    if can_user_delete:
        
        if request.method == 'POST':
            if request.GET.get('id_delete_obj_input') == f'I agree to delete this { auction.title } and take full responsibility for this action.':
                auction.delete()
                return redirect('auctions')
        
        return render(request, 'delete-object.html', {'obj': auction.title})


def auction_like(request, slug, user_id):
    auction = get_object_or_404(Auction, slug=slug)
    user = get_object_or_404(CustomUser, pk=user_id)
    data = {'liked': None}
    if user not in auction.user_likes.all():
        auction.user_likes.add(user)
        data['liked'] = True
    else:
        auction.user_likes.remove(user)
        data['liked'] = False
    
    return JsonResponse(data)


def remind_me(request, slug, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    auction = get_object_or_404(Auction, slug=slug)
    data = {'reminder': None}
    if user not in auction.participants.all():
        auction.participants.add(user)
        data['reminder'] = True
    else:
        auction.participants.remove(user)
        data['reminder'] = False
        
    return JsonResponse(data)


def add_comment(request, slug, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    auction = get_object_or_404(Auction, slug=slug)
    text = request.GET.get('text')
    data = {'added': True}
    new_comment = Comment.objects.create(user=user, auction=auction, text=text)
    
    return JsonResponse(data)


def auction_admins(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    
    auction_admins = auction.permissions.all()
    
    return render(request, 'auctions/auction-admins.html', {'auction_admins': auction_admins, 'auction': auction})


def auction_admin(request, slug, username):
    auction = get_object_or_404(Auction, slug=slug)
    admin = get_object_or_404(CustomUser, username=username)
    
    auction_admin = get_object_or_404(auction.permissions, username=username)
    admin_permissions = auction.auctionuserpermission_set.get(user=admin)
    
    permission_form = AuctionUserPermissionForm(instance=admin_permissions)
    
    if request.method == 'POST':
        permission_form = AuctionUserPermissionForm(request.POST, instance=admin_permissions)
        if permission_form.is_valid() and admin_permissions.can_add_admin and auction_admin != auction.owner:
            permission_form.save()
    
    context = {
        'auction_admin': auction_admin,
        'permission_form': permission_form,
    }
    
    return render(request, 'auctions/auction-admin.html', context)


def auction_admin_delete(request, slug, username):
    auction = get_object_or_404(Auction, slug=slug)
    admin = get_object_or_404(CustomUser, username=username)
    
    auction_admin = get_object_or_404(auction.permissions, username=username)
    if admin != auction.owner:
        permission_form = AuctionUserPermissionForm(instance=admin_permissions).delete()
    
    return redirect('auction-admins', auction.slug)
