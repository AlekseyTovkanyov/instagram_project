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

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        return Response({'status': 'ok'})