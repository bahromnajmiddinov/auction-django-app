from django.urls import path

from .views import UserDetailApiView, UserContactApiView


urlpatterns = [
    path('user/<int:pk>/', UserDetailApiView.as_view(), name='user-detail-api'),
    path('user/contacts/', UserContactApiView.as_view(), name='user-contact-api'),
]
