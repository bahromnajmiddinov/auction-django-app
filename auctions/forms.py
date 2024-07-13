from django import forms
from django.forms import formset_factory
from django.forms.models import inlineformset_factory
from django.utils import timezone

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
    
    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < timezone.now():
            raise forms.ValidationError('Start time must be in the future.')
        return start_time
    
    def clean_end_time(self):
        end_time = self.cleaned_data['end_time']
        start_time = self.cleaned_data['start_time']
        
        if start_time:
            if end_time <= start_time:
                raise forms.ValidationError('End time must be after the start time.')
        
        if end_time <= timezone.now():
            raise forms.ValidationError('End time must be in the future.')
        return end_time


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

