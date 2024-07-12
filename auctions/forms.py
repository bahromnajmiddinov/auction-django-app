from django import forms
from django.forms import formset_factory
from django.forms.models import inlineformset_factory

from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Auction, ImageField, VideoField, AdditionalField, AuctionUserPermission


class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ('main_image', 'type', 'title', 'slug', 'summary', 'description', 'starter_price', 'start_time', 'end_time', 'active', 'categories', 'tags',)
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
        fields = ('video',)


class AdditionalFieldForm(forms.ModelForm):
    class Meta:
        model = AdditionalField
        fields = ['icon', 'title', 'description'] 


class AuctionUserPermissionForm(forms.ModelForm):
    class Meta:
        model = AuctionUserPermission
        fields = ('can_edit', 'can_delete', 'can_add_admin',)


ImageFieldFormset = inlineformset_factory(Auction, ImageField, form=ImageFieldForm, extra=0)
VideoFieldFormset = inlineformset_factory(Auction, VideoField, form=VideoFieldForm, extra=0)
AdditionalFieldFormset = inlineformset_factory(Auction, AdditionalField, form=AdditionalFieldForm, exclude=['auction', 'id'], extra=0)

