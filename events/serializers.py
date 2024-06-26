from rest_framework import serializers
from . import models
from accounts.serializers import UserProfileSimpleSerializer
from accounts.models import Follow as Follower
class EventSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='event-detail', lookup_field='pk')
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    is_following_creator = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = (
            "id",
            "url",
            "author",
            "title",
            "description",
            "media",
            "address",
            "venue",
            "event_form_url",
            "event_start_date",
            "event_start_time",
            "event_end_date",
            "event_end_time",
            "likes_count",
            "comments_count",
            "bookmarks_count",
            "is_liked",
            "is_bookmarked",
            'is_following_creator',
            
            "created_at",
            "updated_at",
        )
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        if data.get('is_online') and data.get('is_physical'):
            raise serializers.ValidationError("An event cannot be both online and physical.")
        if data.get('event_start_date') and data.get('event_end_date') and data['event_start_date'] > data['event_end_date']:
            raise serializers.ValidationError("Event start date cannot be after event end date.")
        return data
    
    def get_likes_count(self, obj):
        return obj.event_likes.count()

    def get_comments_count(self, obj):
        return obj.event_comments.count()
    
    def get_bookmarks_count(self, obj):
        return obj.event_bookmarks.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                user_profile = user.user_profile
                return models.Like.objects.filter(event=obj, author=user_profile).exists()
            except AttributeError:
                raise serializers.ValidationError("User profile is missing.")
            
        return False

    def get_is_bookmarked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                user_profile = user.user_profile
                return models.Bookmark.objects.filter(event=obj, author=user_profile).exists()
            except AttributeError:
                raise serializers.ValidationError("User profile is missing.")
            
        return False
    
    def get_is_following_creator(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                user_profile = user.user_profile
                return Follower.objects.filter(follower=user_profile, followed=obj.author).exists()
            except AttributeError:
                raise serializers.ValidationError("User profile is missing.")
            
        return False



class LikeSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = models.Like
        fields = (
            "id",
            "author",
            "event",
            "created_at"
        )
        read_only_fields = ('created_at',)

class CommentSerializer(serializers.ModelSerializer):
    author = UserProfileSimpleSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            "id",
            "author",
            "event",
            "text",
            "created_at",
            "updated_at"
        )
        read_only_fields = ('created_at', 'updated_at')

class BookmarkSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    author = UserProfileSimpleSerializer(read_only=True)

    class Meta:
        model = models.Bookmark
        fields = (
            "id",
            "author",
            "event",
            "created_at",
            "updated_at"
        )
        read_only_fields = ('created_at', 'updated_at')
