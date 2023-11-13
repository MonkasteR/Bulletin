from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    code = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    TYPE = [
        ("tank", "Танки"),
        ("heal", "Хилы"),
        ("dd", "ДД"),
        ("buyers", "Торговцы"),
        ("gildmaster", "Гильдмастеры"),
        ("quest", "Квестгиверы"),
        ("smith", "Кузнецы"),
        ("tanner", "Кожевники"),
        ("potion", "Зельевары"),
        ("spellmaster", "Мастера заклинаний"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, null=False, blank=False)
    post_time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=16, choices=TYPE, default="tank")
    content = RichTextUploadingField(config_name="special")

    def get_absolute_url(self):
        # return f"/boards/{self.id}/"
        return reverse("post_detail", args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    replay_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="replies"
    )
    status = models.BooleanField(default=None, null=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
