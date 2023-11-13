import datetime

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from Bulletin.settings import SITE_URL, DEFAULT_FROM_EMAIL
from boards.models import Post


@shared_task
def ReadersDigest():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_time__gte=last_week)

    html_content = render_to_string(
        "email/daily_post.html",
        {
            "link": SITE_URL,
            "posts": posts,
        },
    )
    msg = EmailMultiAlternatives(
        subject="Новые объявления за неделю",
        body="",
        from_email=DEFAULT_FROM_EMAIL,
        to=User.objects.all().values_list("email", flat=True),
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
