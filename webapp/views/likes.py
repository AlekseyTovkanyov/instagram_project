from django.shortcuts import get_object_or_404, redirect
from django.views import View
from webapp.models import Post, Like


class ToggleLikeView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
        next_url = request.POST.get('next', 'webapp:index')
        return redirect(next_url)
