from accounts.models import UserProfile
from . import models, serializers
from accounts.pagination import CustomPagination
from .mixins import GetUserProfileAndPostMixin
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsOwnerOrReadOnly

from django.db.models import Q
from rest_framework import filters

# list all posts* // create a new post
class ListCreatePosts(generics.ListCreateAPIView, GetUserProfileAndPostMixin):
    queryset = models.Post.objects.all().order_by('-created_at')
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        serializer.save(author=user_profile)


# retrieve a single instance of post, update and delete
class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all().order_by('-created_at')
    serializer_class = serializers.PostSerializer
    permission_classes = [IsOwnerOrReadOnly]


# get all posts by a specific user
class UserPostsList(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user_id = int(user_id)
            user_profile = UserProfile.objects.get(user__id=user_id)
            return models.Post.objects.filter(author=user_profile).order_by('-created_at')
        except UserProfile.DoesNotExist:
            raise NotFound("UserProfile matching query does not exist.")



# create a new like instance
class CreateLikes(generics.CreateAPIView, GetUserProfileAndPostMixin):
    queryset = models.Like.objects.all().order_by('-created_at')
    serializer_class = serializers.LikedSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        post = self.get_post()
        serializer.save(author=user_profile, post=post)


# retrieve a single instance of like, update and delete
class LikesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Like.objects.all().order_by('-created_at')
    serializer_class = serializers.LikedSerializer
    permission_classes = [IsOwnerOrReadOnly]


# likes count for a post instance
class PostLikesCount(generics.GenericAPIView):
    def get(self, request, post_id, *args, **kwargs):
        try:
            post_id = int(post_id)
            post = models.Post.objects.get(id=post_id)
            likes_count = post.likes.count()
            return Response({"likes_count": likes_count})
        except models.Post.DoesNotExist:
            raise NotFound("Post does not exist")


# get all likes for a specific post instance
class PostLikesList(generics.ListAPIView):
    serializer_class = serializers.LikedSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        try:
            post_id = int(post_id)
            post = models.Post.objects.get(id=post_id)
            return models.Like.objects.filter(post=post).order_by('-created_at')
        except models.Post.DoesNotExist:
            raise NotFound("Post does not exist")


# create a new instance of a comment
class CreateComments(generics.CreateAPIView, GetUserProfileAndPostMixin):
    queryset = models.Comment.objects.all().order_by('-created_at')
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        post = self.get_post()
        serializer.save(author=user_profile, post=post)


# retrieve a single instance of a comment, update and delete
class CommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Comment.objects.all().order_by('-created_at')
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]


# comments count for a post instance
class PostCommentsCount(generics.GenericAPIView):
    def get(self, request, post_id, *args, **kwargs):
        try:
            post_id = int(post_id)
            post = models.Post.objects.get(id=post_id)
            comments_count = post.comments.count()
            return Response({"comments_count": comments_count})
        except models.Post.DoesNotExist:
            raise NotFound("Post does not exist")


# get all comments for a specific post instance
class PostCommentsList(generics.ListAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        try:
            post_id = int(post_id)
            post = models.Post.objects.get(id=post_id)
            return models.Comment.objects.filter(post=post).order_by('-created_at')
        except models.Post.DoesNotExist:
            raise NotFound("Post does not exist")

# create a new bookmark instance
class CreateBookmarks(generics.CreateAPIView, GetUserProfileAndPostMixin):
    queryset = models.Bookmark.objects.all().order_by('-created_at')
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        post = self.get_post()
        serializer.save(author=user_profile, post=post)


# retrieve a single instance of a bookmark, update and delete
class BookmarksDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Bookmark.objects.all().order_by('-created_at')
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [IsOwnerOrReadOnly]


# get all bookmarks by a specific user
class UserBookmarksList(generics.ListAPIView):
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        try:
            user_id = int(user_id)
            user_profile = UserProfile.objects.get(user__id=user_id)
            return models.Bookmark.objects.filter(author=user_profile).order_by('-created_at')
        except UserProfile.DoesNotExist:
            raise NotFound("User profile does not exist")

# bookmarks count for a post instance
class PostBookmarksCount(generics.GenericAPIView):
    def get(self, request, post_id, *args, **kwargs):
        try:
            post = models.Post.objects.get(id=post_id)
            bookmarks_count = post.bookmarks.count()
            return Response({"bookmarks_count": bookmarks_count})
        except models.Post.DoesNotExist:
            raise NotFound("Post does not exist")

# get all bookmarks for a specific post instance
class PostBookmarksList(generics.ListAPIView):
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        try:
            post_id = int(post_id)
            post = models.Post.objects.get(id=post_id)
            return models.Bookmark.objects.filter(post=post).order_by('-created_at')
        except models.Post.DoesNotExist:
            raise NotFound("Post does not exist")



class SearchPosts(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if not query:
            return models.Post.objects.none()
        
        return models.Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-created_at')
