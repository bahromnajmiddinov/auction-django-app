from django import forms
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import SignupForm
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import CustomUser, Address


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('avatar', 'username', 'email', 'first_name', 'last_name', 'description',)
        widgets = {
            'description': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='default'
            ),
        }


class AddressForm(forms.ModelForm):
    class Meta: 
        model = Address
        fields = ['recipient_name', 'street_address', 'city', 'state', 'postal_code', 'country', 'phone_number', 'email', 'instructions', 'is_primary']


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))
    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
