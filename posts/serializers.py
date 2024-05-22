from rest_framework import serializers
from . import models
from accounts import models as account_models


class PostSerializer(serializers.ModelSerializer):
    author=account_models.UserProfile('read_only=True')
    
    class Meta:
        model=models.Post
        fields=(
            "author",
            "title",
            "content",
            "created_at",
            "updated_at"
        )
        
class LikedSerializer(serializers.ModelSerializer):
    user=account_models.UserProfile('read_only=True')
    post=models.Post('read_only=True')
    
    class Meta:
        model=models.Like
        fields=(
            "user",
            "post",
            "created_at"
        )
        
        
class CommentSerializer(serializers.ModelSerializer):
    user=account_models.UserProfile('read_only=True')
    post=models.Post('read_only=True')
    
    class Meta:
        model=models.Like
        fields=(
            "user",
            "post",
            "text",
            "created_at",
            "updated_at"
        )
        
        
class BookmarkSerializer(serializers.ModelSerializer):
    user=account_models.UserProfile('read_only=True')
    post=models.Post('read_only=True')
    
    class Meta:
        model=models.Like
        fields=(
            "user",
            "post",
            "created_at",
            "updated_at"
        )