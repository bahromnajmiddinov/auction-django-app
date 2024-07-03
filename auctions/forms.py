from django import forms
from django.forms import formset_factory

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Auction, ImageField, VideoField, AdditionalField, AuctionUserPermission


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('main_image', 'type', 'title', 'slug', 'description', 'starter_price', 'auction_price', 'start_time', 'end_time', 'active',)
        widgets = {
            'description': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='default'
            ),
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
            ),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False


class ImageFieldForm(forms.ModelForm):
    class Meta:
        model = ImageField
        fields = ('image',)
        

class VideoFieldForm(forms.ModelForm):
    class Meta:
        model = VideoField
        exclude = ('id',)


class AdditionalFieldForm(forms.ModelForm):
    class Meta:
        model = AdditionalField
        exclude = ['id']   


class AuctionUserPermissionForm(forms.ModelForm):
    class Meta:
        model = AuctionUserPermission
        fields = ('can_edit', 'can_delete', 'can_add_admin',)
