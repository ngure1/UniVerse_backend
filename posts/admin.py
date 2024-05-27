from django.contrib import admin
from . import models
class PostAdmin(admin.ModelAdmin):
    list_display=("title", "author", "created_at")

class PostLikeAdmin(admin.ModelAdmin):
    list_display=("post", "owner", "created_at")


class PostCommentAdmin(admin.ModelAdmin):
    list_display=("post", "owner", "created_at")

class PostBookmarkAdmin(admin.ModelAdmin):
    list_display=("post", "owner", "created_at")

  
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Like, PostLikeAdmin)
admin.site.register(models.Comment, PostCommentAdmin)
admin.site.register(models.Bookmark, PostBookmarkAdmin)

