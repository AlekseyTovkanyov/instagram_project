from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from rest_framework.authtoken.models import Token

from accounts.forms.custom_user import CustomUserCreationForm
from webapp.models import Post, Subscription

User = get_user_model()


class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration.html"
    model = User

    def form_valid(self, form):
        user = form.save()
        Token.objects.get_or_create(user=user)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        posts = Post.objects.filter(user=user).annotate(
            likes_count=Count('like_users', distinct=True),
            comments_count=Count('posts_comments', distinct=True)
        )
        context['posts'] = posts
        if self.request.user.is_authenticated:
            context['is_following'] = Subscription.objects.filter(
                follower=self.request.user, followed=user
            ).exists()
        else:
            context['is_following'] = False
        return context


class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        response = super().form_valid(form)
        response.set_cookie('token', token.key)
        return response


class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            try:
                user.auth_token.delete()
            except Token.DoesNotExist:
                pass

        response = super().post(request, *args, **kwargs)
        response.delete_cookie('token')
        return response