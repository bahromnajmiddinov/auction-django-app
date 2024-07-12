from django.urls import path

from . import views


app_name='payments'

urlpatterns = [
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('stripe/<order_id>', views.create_checkout_session, name='stripe'),
]
