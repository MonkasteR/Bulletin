from random import randint

from allauth.core.internal.http import redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView
from django_registration.forms import RegistrationForm

from Bulletin.settings import DEFAULT_FROM_EMAIL
from boards.forms import PostForm
from boards.models import Post, Author


# Create your views here.
class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    permission_required = "boards.add_post"
    template_name = "boards/post_create.html"
    success_message = "Пост был создан"

    def get_success_url(self):
        return reverse("post_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetail(DetailView):
    model = Post
    template_name = "boards/post_detail.html"
    context_object_name = "post_detail"


class PostList(ListView):
    model = Post
    template_name = "boards/post_list.html"
    context_object_name = "post_list"
    paginate_by = 10
    ordering = "-post_time"


def confirmation(request):
    if request.method == "GET":
        code = request.GET.get("confirmation_code")
        account = Author.objects.get(code=code)
        account.user.is_active = True
        account.user.save()
        account.save()
        login(
            request, account.user, backend="django.contrib.auth.backends.ModelBackend"
        )
        return redirect("post_list")
    return render(request, "boards/confirmation.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():  # если валидация прошла успешно
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user_is_author = Group.objects.get(name="Author")
            user.groups.add(user_is_author)

            code = randint(100000, 999999)
            account = Author(user=user, code=code)
            account.save()
            from_email = DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            subj = "Подтверждение регистрации"
            message = f"Код подтверждения: {code}"
            send_mail(subj, message, from_email, recipient_list)
            return redirect("confirmation")
    else:
        form = RegistrationForm()
    return render(request, "boards/registration.html", {"form": form})
