from django.urls import path

from . import views


urlpatterns = [
    path('', views.card_detail, name='card_detail'),
    path('<slug:slug>/add/<user_id>', views.add_to_card, name='add-to-card'),
    path('<slug:slug>/remove/', views.remove_from_card, name='remove-from-card'),
    path('<slug:slug>/delete/', views.delete_from_card, name='delete-from-card'),
]

