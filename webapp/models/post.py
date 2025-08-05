from django.contrib.auth import get_user_model
from django.db import models

from webapp.models.base_model import BaseModel


class Post(BaseModel):
    image = models.ImageField(upload_to='posts', verbose_name='Картинка')
    description = models.TextField(verbose_name="Описание")
    user = models.ForeignKey(get_user_model(), related_name='posts', on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return self.description[:50]

    class Meta:
        db_table = 'posts'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
