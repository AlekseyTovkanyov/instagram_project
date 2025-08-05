from django.contrib.auth import get_user_model
from django.db import models

from webapp.models.base_model import BaseModel


class Like(BaseModel):
    post = models.ForeignKey('webapp.Post', related_name='posts_likes', on_delete=models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(get_user_model(), related_name='users_likes', on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        db_table = 'likes'
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
