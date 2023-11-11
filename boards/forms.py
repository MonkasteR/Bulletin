from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField()

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
        ]
