from django import forms

from .models import Link


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('limit_by_time', 'limit_by_clicks',)
        widgets = {
            'limit_by_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
            ),
        }
