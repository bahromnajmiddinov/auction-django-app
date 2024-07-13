#TODO: add pagination
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Min, Max
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required

import json
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django_filters.views import FilterView

from .utils import get_client_ip, code_to_country_name
from .models import Auction, AuctionUserPermission, LocationData, Comment
from .forms import AuctionForm, AuctionUserPermissionForm
from .forms import ImageFieldFormset, VideoFieldFormset, AdditionalFieldFormset
from accounts.models import CustomUser
from labeler.models import Category, Tag
from .filters import AuctionFilter


def auctions(request):
    if request.user.is_anonymous:
        all_auctions = Auction.objects.filter(type='PB')
    else:
        all_auctions = Auction.objects.filter(Q(type='PB') | Q(user_watchers__in=[request.user]) | (Q(owner__contacts__in=[request.user.id]) & Q(type='OC')))
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    search_input = request.GET.get('search-input')
    min_range_price = request.GET.get('min-range-input')
    max_range_price = request.GET.get('max-range-input')
    selected_categories = request.GET.getlist('category')
    selected_tags = request.GET.getlist('tag')
    
    if search_input:
        all_auctions = all_auctions.filter(title__icontains=search_input)
    
    if min_range_price:
        all_auctions = all_auctions.filter(auction_price__gte=min_range_price)
    
    if max_range_price:
        all_auctions = all_auctions.filter(auction_price__lte=max_range_price)
    
    if selected_categories:
        all_auctions = all_auctions.filter(categories__in=selected_categories)
    
    if selected_tags:
        all_auctions = all_auctions.filter(tags__in=selected_tags)
        
    max_price = all_auctions.aggregate(max_price=Max('auction_price'))['max_price']
    min_price = all_auctions.aggregate(min_price=Min('auction_price'))['min_price']
    
    # Pagination
    paginator = Paginator(all_auctions, 12)
    page = request.GET.get('page', 1)
    all_auctions = paginator.page(page)
    
    context = {
        'all_auctions': all_auctions,
        'categories': categories,
        'tags': tags,
        'max_price': max_price,
        'min_price': min_price,
    }
    
    return render(request, 'auctions/auctions.html', context)


def auction(request, slug):
    auction_detail = get_object_or_404(Auction, slug=slug)
    categories = auction_detail.categories.all()
    tags = auction_detail.tags.all()
    
    if request.user.is_anonymous:
        saved = True if str(auction_detail.id) in request.session.get('cart', []) else False
    else:
        saved = True if request.user.user_cart_items.filter(id=auciton_detail.id).exists() else False
    
    client_ip = get_client_ip(request)
    if client_ip.country is not None:
        client_country = client_ip.country
        client_city = client_ip.city
        ip_address = client_ip.ip
        LocationData.objects.get_or_create(auction=auction_detail, country=client_country, city=client_city, ip_address=ip_address)
    
    if request.user not in auction_detail.user_watchers.all():
        if auction_detail.type != 'PB':
            return Http404()
        if not request.user.is_anonymous:
            auction_detail.user_watchers.add(request.user)
        
    context = {
        'auction': auction_detail,
        'categories': categories,
        'tags': tags,
        'saved': saved,
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


@login_required
def auction_create(request):
    auction_form = AuctionForm()
    
    image_formset = ImageFieldFormset(queryset=None)
    video_formset = VideoFieldFormset()
    additional_formset = AdditionalFieldFormset()
    
    if request.method == 'POST':
        auction_form = AuctionForm(request.POST, request.FILES)
        image_formset = ImageFieldFormset(request.POST, request.FILES)
        video_formset = VideoFieldFormset(request.POST, request.FILES)
        additional_formset = AdditionalFieldFormset(request.POST, request.FILES)
        
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
            
            return redirect('auction', new_auction.slug)
        else:
            print(image_formset.errors)
            
    context = {
        'auction_form': auction_form,
        'image_formset': image_formset,
        'video_formset': video_formset,
        'additional_formset': additional_formset,
    }
    
    return render(request, 'auctions/auction-create-update.html', context)


@login_required
def auction_update(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    can_user_edit = get_object_or_404(AuctionUserPermission, user=request.user, auction=auction).can_edit
    if can_user_edit:
        auction_form = AuctionForm(instance=auction)

        image_formset = ImageFieldFormset(instance=auction)
        video_formset = VideoFieldFormset(instance=auction)
        additional_formset = AdditionalFieldFormset(instance=auction)
        
        if request.method == 'POST':
            auction_form = AuctionForm(request.POST, request.FILES, instance=auction)
            image_formset = ImageFieldFormset(request.POST, request.FILES, instance=auction)
            video_formset = VideoFieldFormset(request.POST, request.FILES, instance=auction)
            additional_formset = AdditionalFieldFormset(request.POST, request.FILES, instance=auction)
            
            print([auction_form.is_valid(), image_formset.is_valid(), video_formset.is_valid(), additional_formset.is_valid()])
            if all([auction_form.is_valid(), image_formset.is_valid(), video_formset.is_valid(), additional_formset.is_valid()]):
                auction_form.save()
                
                image_formset.save()
                video_formset.save()
                additional_formset.save()
                
                return redirect('auction', auction.slug)
            
        context = {
            'auction_form': auction_form,
            'image_formset': image_formset,
            'video_formset': video_formset,
            'additional_formset': additional_formset,
            'auction': auction,
        }
        
        return render(request, 'auctions/auction-create-update.html', context)


@login_required
def auction_delete(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    can_user_delete = get_object_or_404(AuctionUserPermission, user=request.user, auction=auction).can_delete
    if can_user_delete:
        
        if request.method == 'POST':
            if request.GET.get('id_delete_obj_input') == f'I agree to delete this { auction.title } and take full responsibility for this action.':
                auction.delete()
                return redirect('auctions')
        
        return render(request, 'delete-object.html', {'obj': auction.title})


@login_required
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


@login_required
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


@login_required
def add_comment(request, slug, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    auction = get_object_or_404(Auction, slug=slug)
    text = request.GET.get('text')
    data = {'added': True}
    new_comment = Comment.objects.create(user=user, auction=auction, text=text)
    
    return JsonResponse(data)


@login_required
def auction_admins(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    
    auction_admins = auction.permissions.all()
    
    return render(request, 'auctions/auction-admins.html', {'auction_admins': auction_admins, 'auction': auction})


@login_required
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


@login_required
def auction_admins_add(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    auction_slug = auction.slug
    auction_permissions = auction.permissions.values_list('id', flat=True)
    participants = auction.participants.exclude(id__in=auction_permissions)
    
    return render(request, 'auctions/auction-admins-add.html', {'participants': participants, 'auction_slug': auction_slug})


@login_required
def auction_admin_add(request, slug, username):
    auction = get_object_or_404(Auction, slug=slug)
    new_admin = get_object_or_404(CustomUser, username=username)
    
    if new_admin in auction.permissions.all():
        return redirect('auction-admins', auction.slug)
    
    try:
        can_add_admin = auction.auctionuserpermission_set.get(user=request.user).can_add_admin
        
        if not can_add_admin:
            return redirect('auctions')
        
    except AuctionUserPermission.DoesNotExist:
        return redirect('auctions')
    
    permission_form = AuctionUserPermissionForm()
    
    if request.method == 'POST':
        permission_form = AuctionUserPermissionForm(request.POST)
        if permission_form.is_valid():
            permission = permission_form.save(commit=False)
            permission.user = new_admin
            permission.auction = auction
            permission.save()
            
            return redirect('auction-admins', auction.slug)
    
    return render(request, 'auctions/auction-admin.html', {'permission_form': permission_form})


@login_required
def auction_admin_delete(request, slug, username):
    auction = get_object_or_404(Auction, slug=slug)
    admin = get_object_or_404(CustomUser, username=username)
    
    auction_admin = get_object_or_404(auction.permissions, username=username)
    if admin != auction.owner:
        AuctionUserPermission.get(user=auction_admin, auction=auction).delete()
    
    return redirect('auction-admins', auction.slug)
