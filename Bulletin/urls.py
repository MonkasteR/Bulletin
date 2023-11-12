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
from boards import views
from boards.views import (
    PostDetail,
    confirmation,
    register,
    PostDeleteView,
    post_edit,
    reply,
    reply_accept,
    reply_reject,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("boards.urls")),
    # path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/confirmation/", confirmation, name="confirmation"),
    path("accounts/register/", register, name="register"),
    path("accounts/", include("allauth.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("posts/<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("posts/<int:post_id>/edit/", post_edit, name="post_edit"),
    path("posts/<int:post_id>/reply/", reply, name="reply"),
    path("reply/<int:reply_id>/accept/", reply_accept, name="reply_accept"),
    path("reply/<int:reply_id>/reject/", reply_reject, name="reply_reject"),
    path("personal", views.personal, name="personal"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
