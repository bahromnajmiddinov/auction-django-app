from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from django.db import Q

from auctions.models import Auction
from .models import Link
from .forms import LinkForm


def private_links(request, slug):
    auction = get_object_or_404(Auction, slug=slug, type='PR')
    
    if request.user not in auction.permissions.all():
        return redirect('auctions')
    
    all_private_links = auction.link_set.all()
    
    return render(request, 'link_generator/private_links.html', {'all_private_links': all_private_links, 'auction': auction})


def private_link(request, path):
    link = get_object_or_404(Link, path=path)
    if not link.is_expired():
        return HttpResponse('Link expired', status=404)
    
    link.auction.user_watchers.add(request.user)
    
    if request.user not in link.users.all():
        link.users.add(request.user)
    
    return redirect('auction-private', link.auction.slug)


def private_link_delete(request, link_id):
    link = get_object_or_404(Link, id=link_id)
    
    if request.user in link.auction.permissions.all():
        link.delete()
        return redirect('private-links', link.auction.slug)
    
    return redirect('auctions')


def private_link_generate(request, slug):
    auction = get_object_or_404(Auction, slug=slug)
    
    if request.user not in auction.permissions.all():
        return redirect('auctions')
        
    link_form = LinkForm()
    
    if request.method == 'POST':
        link_form = LinkForm(request.POST)
        
        if link_form.is_valid():
            link = link_form.save(commit=False)
            link.auction = auction
            link.save()
            link.users.add(request.user)
            
            return redirect('private-links', auction.slug)
    
    return render(request, 'link_generator/private_link_edit_create.html', {'link_form': link_form})
    