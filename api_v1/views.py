from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api_v1.permissions import IsOwnerOrReadOnly
from api_v1.serializers.post import PostSerializer
from webapp.models import Post


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]


class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if user in post.like_users.all():
            post.like_users.remove(user)
            liked = False
            message = "Like removed"
        else:
            post.like_users.add(user)
            liked = True
            message = "Like added"

        return Response({
            'liked': liked,
            'likes_count': post.like_users.count(),
            'message': message
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        return Response({'status': 'ok'})