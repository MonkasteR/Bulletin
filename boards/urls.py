from django.urls import path

from .views import PostCreateView, PostList

urlpatterns = [
    path("create/", PostCreateView.as_view(), name="add_post"),
    path("", PostList.as_view(), name="post_list"),
]
