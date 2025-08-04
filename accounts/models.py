from django.contrib.auth.models import AbstractUser
from django.db import models

gender_choices = [('M', 'Male'), ('F', 'Female')]


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', verbose_name='Аватар')
    bio = models.TextField(max_length=200, blank=True, null=True, verbose_name='Информация о пользователе')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name='Пол', choices=gender_choices)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "custom_users"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
