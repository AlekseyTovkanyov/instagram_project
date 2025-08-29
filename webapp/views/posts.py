from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, View
from webapp.forms.comments import CommentForm
from webapp.models import Post
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
                likes_count=Count('like_users', distinct=True),
                comments_count=Count('posts_comments', distinct=True)
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
            liked_posts = Post.objects.filter(like_users=self.request.user).values_list('id', flat=True)
            context['liked_posts'] = liked_posts
        return context


class PostCommentView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
        return redirect('webapp:index')


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
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.annotate(
            likes_count=Count('like_users', distinct=True),
            comments_count=Count('posts_comments', distinct=True)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user
        context['likes_count'] = post.like_users.count()
        context['user_liked'] = user in post.like_users.all()
        context['comments_count'] = post.comments_count
        context['form'] = CommentForm()
        context['comments'] = post.posts_comments.all().order_by('created_at')
        return context
