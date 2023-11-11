"""
URL configuration for Bulletin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Bulletin import settings
from boards.views import PostDetail, confirmation, register

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("boards.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/confirmation/", confirmation, name="confirmation"),
    path("accounts/register/", register, name="register"),
    path("accounts/", include("allauth.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("posts/<int:pk>/", PostDetail.as_view(), name="post_detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
