from django import forms
from django.contrib import admin

from boards.models import Post


# Register your models here.


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"


class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "content", "category", "post_time")
    list_filter = ("category", "author")
    search_fields = ("title", "content")
    form = PostAdminForm
    model = Post


admin.site.register(Post, PostAdmin)
