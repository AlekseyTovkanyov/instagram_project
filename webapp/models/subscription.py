from django.contrib.auth import get_user_model
from django.db import models

from webapp.models.base_model import BaseModel


class Subscription(BaseModel):
    follower = models.ForeignKey(get_user_model(), related_name='following', on_delete=models.CASCADE,
                                 verbose_name='Подписчики')
    followed = models.ForeignKey(get_user_model(), related_name='followers', on_delete=models.CASCADE,
                                 verbose_name='Подписанный')

    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
