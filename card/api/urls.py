from django.urls import path

from . import views


urlpatterns = [
    path('', views.CartDetailApiView.as_view(), name='cart-detail-api'),
    path('add/<slug:slug>/', views.AddToCartApiView.as_view(), name='add-to-cart-api'),
]

