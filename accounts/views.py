from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Contact
from .forms import UserUpdateForm


@login_required
def user_detail(request, username=None):
    user = request.user
    user_contact = None
    if username:
        user = get_object_or_404(CustomUser, username=username)
        try:
            user_contact = Contact.objects.get(owner=request.user, user=user)
        except Contact.DoesNotExist:
            pass
    
    return render(request, 'accounts/user-detail.html', {'user': user, 'user_contact': user_contact})


def user_balance(request):
    pass


@login_required
def user_update(request):
    form = UserUpdateForm(instance=request.user)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            
            return redirect('user-detail')
    
    return render(request, 'accounts/user-update.html', {'form': form})


@login_required
def user_delete(request):
    obj = 'account'
    check_text = request.POST.get('check_text' or None)
    if check_text == f'I agree to delete this {obj} and take full responsibility for this action.':
        request.user.delete()
        return redirect('account_login')

    return render(request, 'delete-object.html', {'obj': obj})


@login_required
def user_contacts(request):
    user_contacts = request.user.contacts.all()
    
    return render(request, 'accounts/user-contacts.html', {'user_contacts': user_contacts})


@login_required
def user_save_contact(request, other_username):
    contact = get_object_or_404(CustomUser, username=other_username)
    contact_errors = {}
    
    if request.user == contact:
        return redirect('user-detail', request.user.username)
    
    if request.method == 'POST':
        first_name = request.POST.get('contact_first_name').strip()
        last_name = request.POST.get('contact_last_name').strip()
        
        if first_name:
            Contact.objects.get_or_create(first_name=first_name, last_name=last_name, owner=request.user, user=contact)
            return redirect('user-detail', contact.username)

        contact_errors = {'first_name': 'Please Enter First Name!'}
    
    return render(request, 'accounts/user-contact-update-create.html', {'contact': contact, 'contact_errors': contact_errors})


@login_required
def user_update_contact(request, other_username):
    other_user = get_object_or_404(CustomUser, username=other_username)
    contact_errors = {}
    
    try:
        contact = Contact.objects.get(owner=request.user, user=other_user)
        if request.method == 'POST':
            first_name = request.POST.get('contact_first_name').strip()
            last_name = request.POST.get('contact_last_name').strip()
            
            if first_name:
                contact.first_name = first_name
                contact.last_name = last_name
                contact.save()
                return redirect('user-detail', other_user.username)
            
            contact_errors = {'first_name': 'Please Enter First Name!'}
            
    except Contact.DoesNotExist:
        return redirect('user-save-contact', other_username)
    
    return render(request, 'accounts/user-contact-update-create.html', {'contact': contact, 'contact_errors': contact_errors})


@login_required
def user_delete_contact(request, other_username):
    other_user = get_object_or_404(CustomUser, username=other_username)
    
    try:
        contact = Contact.objects.get(owner=request.user, user=other_user)
        if request.method == 'POST':
            if request.POST.get('check_text') == f'I agree to delete this { contact.first_name } and take full responsibility for this action.':
                contact.delete()
                return redirect('user-contacts')
    except Contact.DoesNotExist:
        return redirect('user-save-contact', other_username)
    
    return render(request, 'delete-object.html', {'obj': contact.first_name})
