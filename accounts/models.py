from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field
from django_countries.fields import CountryField 


USER_ACCOUNT_TYPE_CHOICES = (
    ('PB', _('PUBLIC')),
    ('PR', _('PRIVATE')),
)


def customuser_avatar_path (instance, filename):
    ext = filename.split('.')[-1]
    path = f'media/users/{instance.id}/images/avatars/avatar.{ext}'
    return path


class CustomUser(AbstractUser):
    type = models.CharField(_('Type'), max_length=2, choices=USER_ACCOUNT_TYPE_CHOICES, default='PB')
    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50)
    avatar = models.ImageField(_('Avatar'), upload_to=customuser_avatar_path, blank=True, null=True)
    description = CKEditor5Field(_('Description'), config_name='default')
    
    def __str__(self):
        return f'{self.username} | {self.type}'
    
    @property
    def get_avatar_url(self):
        return self.avatar.url if self.avatar else static('images/users/default-avatar.svg')


class Contact(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contacts', verbose_name=_('Owner'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users_that_saved_me', verbose_name=_('User'))
    first_name = models.CharField(_('First Name'), max_length=50)
    last_name = models.CharField(_('Last Name'), max_length=50)


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('User'))
    recipient_name = models.CharField(_('Recipient Name'), max_length=255)
    street_address = models.CharField(_('Street Address'), max_length=255)
    city = models.CharField(_('City'), max_length=255)
    state = models.CharField(_('State'), max_length=100)
    postal_code = models.CharField(_('Postal Code'), max_length=20)
    country = CountryField(verbose_name=_('Country'))
    phone_number = models.CharField(_('Phone Number'), max_length=20)
    email = models.EmailField(_('Email'), blank=True)
    instructions = models.TextField(_('Instructions'), blank=True)
    is_primary = models.BooleanField(_('Is Primary'), default=False)

    def __str__(self):
        return f"{self.recipient_name} - {self.street_address}, {self.city}, {self.country}"

    class Meta:
        verbose_name_plural = 'Addresses'
