from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'avatar', 'first_name', 'bio', 'phone_number', 'gender']
    list_display_links = ['id', 'username']
    list_filter = ['gender']
    search_fields = ['username', 'bio']
    fields = ['username', 'email', 'avatar', 'first_name', 'bio', 'phone_number', 'gender']


admin.site.register(User, CustomUserAdmin)
