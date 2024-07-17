from django.urls import path

from . import views


urlpatterns = [
    path('order/checkout/', views.checkout, name='checkout-api'),
    path('order/', views.order_data, name='order-data-api'),
    path('order/<order_id>/', views.order_data, name='order-data-api'),
]

