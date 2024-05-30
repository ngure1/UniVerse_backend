from django.contrib import admin
from . import models

admin.site.site_header = "UniVerse Admin"
admin.site.site_title = "UniVerse Admin Area"
admin.site.index_title = "Welcome to the UniVerse Admin Area"

# List dsplay for UniVerse_Post_Admin
class PostAdmin(admin.ModelAdmin):
    list_display=("title", "author", "created_at")
    search_fields = ('title', 'author')

class PostLikeAdmin(admin.ModelAdmin):
    list_display=("post", "owner", "created_at")


class PostCommentAdmin(admin.ModelAdmin):
    list_display=("post", "owner", "created_at")
    search_fields = ('post', 'owner')

class PostBookmarkAdmin(admin.ModelAdmin):
    list_display=("post", "owner", "created_at")
    search_fields = ('post', 'owner')

# Register your models here.
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Like, PostLikeAdmin)
admin.site.register(models.Comment, PostCommentAdmin)
admin.site.register(models.Bookmark, PostBookmarkAdmin)

