from django.urls import path

from . import views


urlpatterns = [
    path('<slug:slug>/', views.PrivateLinkListApiView.as_view(), name='private-links-api'),
    path('link/<path>/', views.PrivateLinkDetailApiView.as_view(), name='private-link'),
]

