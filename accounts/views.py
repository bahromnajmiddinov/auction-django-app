from django.shortcuts import render, get_object_or_404

from .models import CustomUser


def user_detail(request, username=None):
    user = request.user
    if username:
        user = get_object_or_404(CustomUser, username=username)
    
    return render(request, 'accounts/user-detail.html', {'user': user})

def user_balance(request):
    pass


def user_dashboard(request):
    pass


def user_update(request):
    pass


def user_logout(request):
    pass


def user_delete(request):
    pass


def user_contacts(request):
    pass


def user_save_contact(request):
    pass


def user_update_contact(request):
    pass


def user_delete_contact(request):
    pass
