from django.urls import path

from . import views


urlpatterns = [
    path('', views.card_detail, name='card-detail'),
    path('<slug:slug>/add/', views.add_to_card, name='add-to-card'),
    path('<slug:slug>/remove/', views.remove_from_card, name='remove-from-card'),
]

