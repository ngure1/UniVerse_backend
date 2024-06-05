from rest_framework import serializers
from . import models
from accounts.serializers import UserProfileSerializer

#1
class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    
    url = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='pk')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = (
            "url",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
            "likes_count",
            "comments_count",
            "is_liked",
            "is_bookmarked",
        )
        read_only_fields = ('created_at', 'updated_at')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return models.Like.objects.filter(post=obj, owner=user).exists()
        return False

    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return models.Bookmark.objects.filter(post=obj, owner=user).exists()
        return False

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
        read_only_fields=('created_at',)
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
        model=models.Bookmark
        fields=(
            "id",
            "owner",
            "post",
            "created_at",
            "updated_at"
        )
        read_only_fields=('created_at', 'updated_at')