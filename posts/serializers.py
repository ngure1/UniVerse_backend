from rest_framework import serializers
from . import models
from accounts.serializers import UserProfileSerializer

#1
class PostSerializer(serializers.ModelSerializer):
    author=UserProfileSerializer(read_only=True)
    class Meta:
        model=models.Post
        fields=(
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = ('created_at', 'updated_at')
    
# 2
class LikedSerializer(serializers.ModelSerializer):
    owner=UserProfileSerializer(read_only=True)
    post=PostSerializer(read_only=True)
    
    class Meta:
        model=models.Like
        fields=(
            "id",
            "owner",
            "post",
            "created_at"
        )
        read_only_fields=('created_at')
#3
class CommentSerializer(serializers.ModelSerializer):
    owner=UserProfileSerializer(read_only=True)
    post=PostSerializer(read_only=True)
    
    class Meta:
        model=models.Comment
        fields=(
            "id",
            "owner",
            "post",
            "text",
            "created_at",
            "updated_at"
        )
        read_only_fields=('created_at', 'updated_at')

#4
class BookmarkSerializer(serializers.ModelSerializer):
    owner=UserProfileSerializer(read_only=True)
    post=PostSerializer(read_only=True)
    
    class Meta:
        model=models.Like
        fields=(
            "id",
            "owner",
            "post",
            "created_at",
            "updated_at"
        )
        read_only_fields=('created_at', 'updated_at')