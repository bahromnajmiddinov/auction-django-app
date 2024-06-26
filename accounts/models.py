from django.db import models
from django.contrib.auth.models import AbstractUser

from django_ckeditor_5.fields import CKEditor5Field


USER_ACCOUNT_TYPE_CHOICES = (
    ('PB', 'PUBLIC',),
    ('PR', 'PRIVATE'),
)


def customuser_avatar_path (instance, filename):
    ext = filename.split('.')[-1]
    path = f'media/users/{instance.id}/images/avatars/avatar.{ext}'
    return path


class CustomUser(AbstractUser):
    type = models.CharField(max_length=2, choices=USER_ACCOUNT_TYPE_CHOICES, default='PB')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to=customuser_avatar_path, blank=True, null=True)
    description = CKEditor5Field('Text', config_name='default')
    
    def __str__(self):
        return f'{self.username} | {self.type}'


class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
