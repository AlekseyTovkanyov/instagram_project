from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from webapp.models import Post, Like
from webapp.forms import PostForm

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            followed_users = User.objects.filter(followers__follower=self.request.user)
            queryset = Post.objects.filter(user__in=followed_users).order_by('-created_at').annotate(
                likes_count=Count('posts_likes'),
                comments_count=Count('posts_comments')
            )
        else:
            queryset = Post.objects.none()
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
        if self.request.user.is_authenticated:
            liked_posts = Like.objects.filter(user=self.request.user).values_list('post_id', flat=True)
            context['liked_posts'] = liked_posts
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user
        post_with_counts = Post.objects.filter(id=post.id).annotate(
            likes_count=Count('posts_likes'),
            comments_count=Count('posts_comments')
        ).first()
        context['likes_count'] = post_with_counts.likes_count
        context['comments_count'] = post_with_counts.comments_count
        context['user_liked'] = Like.objects.filter(user=user, post=post).exists()
        return context
