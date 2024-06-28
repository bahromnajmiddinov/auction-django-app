from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import Link


def private_link(request, path):
    link = get_object_or_404(Link, path=path)
    if link.is_expired():
        return HttpResponse('Link expired', status=404)
    
    link.auction.user_watchers.add(request.User)
    
    return redirect('auction', link.auction.slug)
    