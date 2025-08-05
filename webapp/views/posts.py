from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from webapp.models import Post
from webapp.forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'posts/posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.annotate(
            likes_count=Count('posts_likes'),
            comments_count=Count('posts_comments')
        )


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
