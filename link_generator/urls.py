from django.urls import path

from . import views


urlpatterns = [
    path('link/private/<path>', views.private_link, name='private-link'),
    path('link/private/generate/<slug:slug>', views.private_link_generate, name='generate-link'),
    path('link/private/delete/<link_id>', views.private_link_delete, name='delete-link'),
    path('links/<slug:slug>', views.private_links, name='private-links'),
]

