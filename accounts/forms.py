from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import CustomUser


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('avatar', 'username', 'email', 'first_name', 'last_name', 'description',)
        widgets = {
            'description': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='default'
            ),
        }