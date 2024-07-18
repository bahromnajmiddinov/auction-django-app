from django.urls import path

from .views import (UserDetailApiView, UserContactApiView, 
                    UserContactsDetailApiView, UserAddressApiView, 
                    UserAddressDetailApiView)

urlpatterns = [
    path('user/<int:pk>/', UserDetailApiView.as_view(), name='user-detail-api'),
    path('user/contacts/', UserContactApiView.as_view(), name='user-contacts-api'),
    path('user/contacts/contact/<user_id>/', UserContactsDetailApiView.as_view(), name='user-contact-detail-api'),
    path('user/addresses/', UserAddressApiView.as_view(), name='user-addresses-api'),
    path('user/addresses/address/<address_id>/', UserAddressDetailApiView.as_view(), name='user-address-detail-api'),
]
