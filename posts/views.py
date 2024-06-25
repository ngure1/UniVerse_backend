from accounts.models import UserProfile
from . import models, serializers
from accounts.pagination import CustomPagination
from .mixins import GetUserProfileAndPostMixin
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsOwnerOrReadOnly

from django.db.models import Q
from rest_framework import filters

# list all posts* // create a new post
class ListCreatePosts(generics.ListCreateAPIView, GetUserProfileAndPostMixin):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        serializer.save(author=user_profile)
        
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return models.Post.objects.exclude(author=user.user_profile).order_by('-created_at')
        else:
            return models.Post.objects.all().order_by('-created_at')



    # retrieve a single instance of post, update and delete
class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all().order_by('-created_at')
    serializer_class = serializers.PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    



    # get all posts by the current logged in user   (no id needed)
class CurrentUserPostsList(generics.ListAPIView, GetUserProfileAndPostMixin):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class=CustomPagination

    def get_queryset(self):
        # Get the current logged-in user's profile
        user_profile = self.get_user_profile()
        # Filter posts by this user profile
        return models.Post.objects.filter(author=user_profile).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "The current user has no posts."}, status=status.HTTP_204_NO_CONTENT)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    
# get all posts by a specific user  -id needed
class UserPostsList(generics.ListAPIView, GetUserProfileAndPostMixin):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user_profile = self.get_user_profile_by_id(user_id)
        posts = models.Post.objects.filter(author=user_profile).order_by('-created_at')
        if not posts.exists():
            raise NotFound("This user does not have any posts.")
        return posts




    #Like a post
class CreateLikes(generics.CreateAPIView, GetUserProfileAndPostMixin):
    queryset = models.Like.objects.all().order_by('-created_at')
    serializer_class = serializers.LikedSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        post = self.get_post()
        
        # Check if the user has already liked the post
        if models.Like.objects.filter(post=post, author=user_profile).exists():
            raise NotFound("You have already liked this post.")
        
        serializer.save(author=user_profile, post=post)


    # unlike a post
class UnlikePost(generics.GenericAPIView, GetUserProfileAndPostMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, post_id, *args, **kwargs):
        
        user_profile = self.get_user_profile()
        post = self.get_post()

        try:
            like = models.Like.objects.get(post=post, author=user_profile)
            like.delete()
            return Response({"detail": "Unliked the post successfully."}, status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)


    # get all likes for a specific post
class PostLikesList(generics.ListAPIView, GetUserProfileAndPostMixin):
    serializer_class = serializers.LikedSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        post = self.get_post()
        likes = models.Like.objects.filter(post=post)
        if not likes.exists():
            raise NotFound("This post does not have any likes.")
        return likes



    # Comment on a post
class CreateComments(generics.CreateAPIView, GetUserProfileAndPostMixin):
    queryset = models.Comment.objects.all().order_by('-created_at')
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        post = self.get_post()
        
        # Check if the user has already commented on the post
        if models.Comment.objects.filter(post=post, author=user_profile).exists():
            raise NotFound("You have already commented on this post.")
        
        serializer.save(author=user_profile, post=post)
        
        

    #delete a comment
class DeleteComment(generics.GenericAPIView, GetUserProfileAndPostMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, post_id, *args, **kwargs):
        
        user_profile = self.get_user_profile()
        post = self.get_post()

        try:
            comment = models.Comment.objects.get(post=post, author=user_profile)
            comment.delete()
            return Response({"detail": "Deleted the comment successfully."}, status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response({"detail": "Comment does not exist or you are not the author of the comment."}, status=status.HTTP_400_BAD_REQUEST)


    #list all comments for a specific post
class PostCommentsList(generics.ListAPIView, GetUserProfileAndPostMixin):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        post = self.get_post()
        comments = models.Comment.objects.filter(post=post)
        if not comments.exists():
            raise NotFound("This post does not have any comments.")
        return comments

    #Bookmark a post
class CreateBookmarks(generics.CreateAPIView, GetUserProfileAndPostMixin):
    queryset = models.Bookmark.objects.all().order_by('-created_at')
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        post = self.get_post()
        
        # Check if the user has already bookmarked the post
        if models.Bookmark.objects.filter(post=post, author=user_profile).exists():
            raise NotFound("You have already bookmarked this post.")
        
        serializer.save(author=user_profile, post=post)

        
        
        
    # unbookmark a post
class UnbookmarkPost(generics.GenericAPIView, GetUserProfileAndPostMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request,*args, **kwargs):
        
        user_profile = self.get_user_profile()
        post = self.get_post()


        try:
            bookmark = models.Bookmark.objects.get(post=post, author=user_profile)
            bookmark.delete()
            return Response({"detail": "Unbookmarked the post successfully."}, status=status.HTTP_204_NO_CONTENT)
        except models.Bookmark.DoesNotExist:
            return Response({"detail": "Bookmark does not exist."}, status=status.HTTP_400_BAD_REQUEST)


# get all bookmarks by a specific user
class UserBookmarksList(generics.ListAPIView, GetUserProfileAndPostMixin):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if not user_id:
            raise NotFound("User ID not provided.")
        user_profile = self.get_user_profile_by_id(user_id)
        bookmarked_posts = models.Post.objects.filter(bookmarks__author=user_profile).order_by('-created_at') # get all posts that have been bookmarked by this user
        if not bookmarked_posts.exists():
            raise NotFound("This user does not have any bookmarked posts.")
        return bookmarked_posts

    # get all bookmarks by the current logged in  user
class CurrentUserBookmarksList(generics.ListAPIView, GetUserProfileAndPostMixin):
    serializer_class = serializers.PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_profile = self.get_user_profile()
        bookmarked_posts = models.Post.objects.filter(bookmarks__author=user_profile).order_by('-created_at') # get all posts that have been bookmarked by this user
        return bookmarked_posts

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
