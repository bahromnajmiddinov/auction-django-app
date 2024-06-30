from django.urls import path

from . import views


urlpatterns = [
    path('account/', views.user_detail, name='user-detail'),
    path('account/<str:username>', views.user_detail, name='user-detail'),
    path('account/user-balance/', views.user_balance, name='user-balance'),
    path('account/user-update/', views.user_update, name='user-update'),
    path('account/user-delete/', views.user_delete, name='user-delete'),
    
    path('account/user-contacts/', views.user_contacts, name='user-contacts'),
    path('account/user-contacts/contact/@<other_username>/save/', views.user_save_contact, name='user-save-contact'),
    path('account/user-contacts/contact/@<other_username>/update/', views.user_update_contact, name='user-update-contact'),
    path('account/user-contacts/contact/@<other_username>/delete/', views.user_delete_contact, name='user-delete-contact'),
]
