from django.contrib import admin

from webapp.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'created_at']
    list_display_links = ['id', 'description']
    search_fields = ['description']
    fields = ['image', 'description']
    readonly_fields = ['user', 'created_at', 'updated_at']


admin.site.register(Post, PostAdmin)
