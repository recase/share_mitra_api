"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from user.views import UserActivateInvalidTemplateView, UserActivateSuccessTemplateView, activate_email
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls', namespace="user")),
    path('api/', include('stock_api.urls', namespace="stock_api")),
    path('api/', include('portfolio.urls', namespace="portfolio_api")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('activate-email/<uidb64>/<token>',
         activate_email, name="activate_email"),
    path('user-activated', UserActivateSuccessTemplateView.as_view(),
         name="user_activated"),
    path('activate-invalid', UserActivateInvalidTemplateView.as_view(),
         name="invalid_activation"),
    path('doc', include_docs_urls(title="shareMitraAPI"))

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
