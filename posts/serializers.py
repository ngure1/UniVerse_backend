from rest_framework import serializers
from . import models
from accounts.serializers import UserProfileSimpleSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='pk')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    is_following_creator = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = (
            "id",
            "url",
            "author",
            "title",
            "content",
            "media",
            "likes_count",
            'is_following_creator',
            "comments_count",
            "is_liked",
            "is_bookmarked",
            "created_at",
            "updated_at",
        )
        read_only_fields = ('created_at', 'updated_at')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                user_profile = user.user_profile
                return models.Like.objects.filter(post=obj, author=user_profile).exists()
            except AttributeError:
                # Handle the case where the user does not have a profile
                pass
        return False

    def get_is_following_creator(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                user_profile = user.user_profile
                return models.Follower.objects.filter(follower=user_profile, followed=obj.author).exists()
            except AttributeError:
                # Handle the case where the user does not have a profile
                pass
        return False


    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                user_profile = user.user_profile
                return models.Bookmark.objects.filter(post=obj, author=user_profile).exists()
            except AttributeError:
                # Handle the case where the user does not have a profile
                pass
        return False

class PostSimpleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='pk')

    class Meta:
        model = models.Post
        fields = (
            "id",
            "url",
            "title",
        )


class LikedSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    post = PostSimpleSerializer(read_only=True)

    class Meta:
        model = models.Like
        fields = (
            "id",
            "author",
            "post",
            "created_at"
        )
        read_only_fields = ('created_at',)

class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    post = PostSimpleSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            "id",
            "author",
            "post",
            "text",
            "created_at",
            "updated_at"
        )
        read_only_fields = ('created_at', 'updated_at')

class BookmarkSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    post = PostSimpleSerializer(read_only=True)

    class Meta:
        model = models.Bookmark
        fields = (
            "id",
            "author",
            "post",
            "created_at",
            "updated_at"
        )
        read_only_fields = ('created_at', 'updated_at')
