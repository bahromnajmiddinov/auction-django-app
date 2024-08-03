from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    
    def __str__(self):
        return self.name
