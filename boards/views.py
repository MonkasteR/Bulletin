from random import randint

from allauth.core.internal.http import redirect
from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, DeleteView
from django_registration.forms import RegistrationForm

from Bulletin.settings import DEFAULT_FROM_EMAIL
from boards.forms import PostForm
from boards.models import Post
from .models import Author


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


def post_edit(request, post_id=None):  # редактировать объявление
    item = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect("post_detail", pk=post_id)
    return render(request, "boards/post_edit.html", {"form": form})

    # Обновляем поля новости с новыми данными
    # post.title = request.POST.get("title")
    # post.content = request.POST.get("content")

    # Сохраняем изменения в базу данных

    # Перенаправляем пользователя на страницу с деталями новости
    # return redirect("post_detail", id=post_id)


class PostDetail(DetailView):
    model = Post
    template_name = "boards/post_detail.html"
    context_object_name = "post_detail"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавьте код для добавления данных в контекст
        context[
            "post_detail"
        ] = self.get_object()  # Пример добавления объекта 'post' в контекст
        return context


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = "boards.delete_post"
    template_name = "boards/post_confirm_delete.html"
    success_message = "Пост был удален"
    success_url = reverse_lazy("post_list")


class PostList(ListView):
    model = Post
    template_name = "boards/post_list.html"
    context_object_name = "post_list"
    paginate_by = 10
    ordering = "-post_time"


def confirmation(request):
    if request.method == "POST":
        code = request.POST.get("confirmation_code")
        try:
            account = Author.objects.get(code=code)
        except Author.DoesNotExist:
            return HttpResponse("Неверный код подтверждения.")

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
        print("POST", request.POST)  # TODO удалить
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("valid", form.cleaned_data)
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
            subj = "Вы успешно зарегистрировались!"
            message = f"Код подтверждения: {code}"
            send_mail(subj, message, from_email, recipient_list)

            return redirect("confirmation")
    else:
        form = RegistrationForm()

    return render(request, "boards/registration.html", {"form": form})
