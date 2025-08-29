from rest_framework import serializers

from webapp.models.post import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'image', 'description', 'created_at', 'updated_at', 'user', 'like_users']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'like_users']
