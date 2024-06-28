from django.urls import path

from . import views


urlpatterns = [
    path('link/private/<path>', views.private_link, name='private-link'),
]

