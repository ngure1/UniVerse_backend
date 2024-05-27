from django.db import models
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    author=models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="posts")
    title=models.CharField(_("Post Title"),max_length=255)
    content=models.CharField(_("Post contents"), max_length=255)
    created_at=models.DateTimeField( _("Date Created"), auto_now_add=True)
    updated_at=models.DateTimeField(_("Date Updated"), auto_now=True)
    
    def __str__(self):
        return self.title
    

    

class Like(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    owner=models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    
    def __str__(self):
        return f"{self.owner.user.first_name} likes {self.post.title}"
    
class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    owner=models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="comments")
    text=models.CharField(_("Comment Text"), max_length=255)
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at=models.DateTimeField(_("Date Updated"), auto_now=True)
    
    def __str__(self):
        return f"{self.owner.user.first_name} on {self.post.title}: {self.text[:20]}"

    
    
class Bookmark(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    owner=models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE, related_name="bookmarks")
    created_at=models.DateTimeField( _("Date Created"), auto_now_add=True)
    updated_at=models.DateTimeField(_("Date Updated"), auto_now=True)
    
    def __str__(self):
        return f"{self.owner.user.first_name} bookmarked {self.post.title}"
    