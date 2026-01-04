"""
URL configuration for comm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static
from comm import settings

urlpatterns = [
    # Built-in URLs
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # Domain URLs
    path("api/v1/comments/", include("app.comments.api.urls"), name="comments"),
    path("api/v1/accounts/", include("app.accounts.api.urls"), name="accounts"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
