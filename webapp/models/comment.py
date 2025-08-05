from django.contrib.auth import get_user_model
from django.db import models

from webapp.models.base_model import BaseModel


class Comment(BaseModel):
    post = models.ForeignKey('webapp.Post', related_name='posts_comments', on_delete=models.CASCADE,
                             verbose_name='Пост')
    text = models.TextField(verbose_name="Текст комментария")
    user = models.ForeignKey(get_user_model(), related_name='posts_users', on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        db_table = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
