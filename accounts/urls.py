from django.urls import path

from . import views


urlpatterns = [
    path('account/', views.user_detail, name='user-detail'),
    path('account/<str:username>', views.user_detail, name='user-detail'),
    path('account/user-update/', views.user_update, name='user-update'),
    path('account/user-delete/', views.user_delete, name='user-delete'),
    
    path('account/user-contacts/', views.user_contacts, name='user-contacts'),
    path('account/user-contacts/contact/@<other_username>/save/', views.user_save_contact, name='user-save-contact'),
    path('account/user-contacts/contact/@<other_username>/update/', views.user_update_contact, name='user-update-contact'),
    path('account/user-contacts/contact/@<other_username>/delete/', views.user_delete_contact, name='user-delete-contact'),
    
    path('account/user-addresses/', views.user_addresses, name='user-addresses'),
    path('account/user-addresses/address/add/', views.user_address_add, name='address-add'),
    path('account/user-addresses/address/<id>/update/', views.user_address_update, name='address-update'),
    path('account/user-addresses/address/<id>/delete/', views.user_address_delete, name='address-delete'),
]
