"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from auctions.views import auctions


schema_view = get_schema_view(
    openapi.Info(
        title="OnAuc API",
        default_version='v1',
        description="OnAuc is a Django-based online auction platform that offers a robust user experience with features such as user authentication, auction creation, bidding, and real-time chat.",
        contact=openapi.Contact(email="najmiddinovbahrom402@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)


api_urlpatterns = [
    path('api/v1/users/', include('accounts.api.urls')),
    path('api/v1/auctions/', include('auctions.api.urls')),
    path('api/v1/dashboard/', include('dashboard.api.urls')),
    path('api/v1/links/', include('link_generator.api.urls')),
    path('api/v1/cart/', include('card.api.urls')),
    path('api/v1/orders/', include('order.api.urls')),  
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns = [
    path('', auctions),
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('auctions/', include('auctions.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', include('link_generator.urls')),
    path('card/', include('card.urls')),
    path('orders/', include('order.urls')),
    path('payment/', include('payments.urls', namespace='payments')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += api_urlpatterns
