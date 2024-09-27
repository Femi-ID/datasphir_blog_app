from django.contrib import admin
from .models import BlogPost, Comments

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'body', 'likes')
    list_filter = ('owner',)

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'post', 'body', 'likes')
    list_filter = ('owner',)