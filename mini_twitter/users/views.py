from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import CustomUserCreationForm, LoginForm, ChangeUserInfo, ChangeUserProfile
from .models import User, UserProfile


class UserList(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        users = super().get_queryset().select_related('profile')
        return users

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['following'] = self.request.user.following.all()
        return context


# def user_detail(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     context = {"user": user}
#     return render(request, "users/user_detail.html", context)

class UserDetail(DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user_info'

    def get_queryset(self):
        return super().get_queryset().select_related('profile').annotate(
            followers_count=Count('followers', distinct=True),
            following_count=Count('following', distinct=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['user_info']
        context['followers'] = user.followers.all().select_related('profile')
        context['following'] = user.following.all().select_related('profile')
        return context


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('posts_list')
    template_name = 'users/registration.html'

    def form_valid(self, form):
        to_return = super().form_valid(form)
        UserProfile.objects.create(user=self.object)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        return to_return


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('posts_list')
    else:
        form = LoginForm(request)
    return render(request, 'users/login.html', context={'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


class ChangeInfo(UpdateView):
    form_class = ChangeUserInfo
    template_name = 'users/change_user_info.html'
    model = User

    def form_valid(self, form):
        form.instance.user = self.request.user  # Передаємо користувача
        return super().form_valid(form)


class ChangeProfile(UpdateView):
    form_class = ChangeUserProfile
    template_name = 'users/change_profile.html'
    model = UserProfile

    def form_valid(self, form):
        form.instance.user = self.request.user  # Передаємо користувача
        return super().form_valid(form)


def subscribe(request, pk):
    user_follow = get_object_or_404(User, pk=pk)
    request.user.following.add(user_follow)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unsubscribe(request, pk):
    user_follow = get_object_or_404(User, pk=pk)
    request.user.following.remove(user_follow)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def password_reset_request(request):
    if request.method == "POST":
        print("post")
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            mail = password_reset_form.cleaned_data['email']
            try:
                user = User.objects.get(email=mail)
            except Exception:
                user = False
            if user:
                subject = 'Запит на скидання пароля'
                email_template_name = "users/password_reset_msg.html"
                print(user.email)
                cont = {
                    "email": user.email,
                    "domain": '127.0.0.1:8000',
                    "site_name": 'Сайт',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": default_token_generator.make_token(user),
                    "protokol": 'http',
                }
                msg_html = render_to_string(email_template_name, cont)
                print(cont['uid'], cont['token'])
                try:
                    # msg = EmailMessage(subject,
                    #                    msg_html, to=[user.email])
                    # msg.send()
                    # print(msg.connection)
                    req = send_mail(subject, 'посилання', 'i3oi3ka@ukr.net', [user.email],
                                    fail_silently=True, html_message=msg_html)
                    print("листа відправлено ", req)
                except BadHeaderError:
                    return HttpResponse('Виявлено недопустимий заголовок')
                return redirect("password_reset_done")
            else:
                messages.error(request, 'користувача не знайдено, напишіть адміністратору')
                return redirect('password_reset')
    return render(request=request, template_name='users/password_reset.html')
