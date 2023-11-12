from django.conf.urls.static import static
from django.urls import path

from Bulletin import settings
from .views import PostCreateView, PostList

urlpatterns = [
    path("create/", PostCreateView.as_view(), name="add_post"),
    path("", PostList.as_view(), name="post_list"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
