from django.urls import path

from . import views


urlpatterns = [
    path('order/checkout/', views.checkout, name='checkout'),
    path('order/order-data/', views.order_data, name='order-data'),
]