from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from webapp.models import Post
from webapp.forms import PostForm

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset().annotate(
            likes_count=Count('posts_likes'),
            comments_count=Count('posts_comments')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        if query:
            users = User.objects.filter(
                Q(username__icontains=query) |
                Q(email__icontains=query) |
                Q(first_name__icontains=query)
            )
            context['users'] = users
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
