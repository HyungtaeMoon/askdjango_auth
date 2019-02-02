from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']
    # admin 페이지에서 키워드로 search 기능
    search_fields = ['title']
