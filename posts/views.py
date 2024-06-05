from . import models
from . import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from accounts.models import UserProfile
from django.db.models import Q
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

   # list all posts* // create a new post
class ListCreatePosts(generics.ListCreateAPIView):
    queryset=models.Post.objects.all()
    serializer_class=serializers.PostSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        serializer.save(author=user_profile)


  # retrieve a sigle instance of post, update and delete
class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Post.objects.all()
    serializer_class=serializers.PostSerializer
    permission_classes=[IsOwnerOrReadOnly]



   #  get all posts by a specific user
class UserPostsList(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user_profile = UserProfile.objects.get(user__id=user_id)
        return models.Post.objects.filter(author=user_profile)
    
    
        # create a new like//list all likes*
class ListCreateLikes(generics.ListCreateAPIView):
    queryset=models.Like.objects.all()
    serializer_class=serializers.LikedSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    
    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        serializer.save(owner=user_profile)
    
    
    # retrieve a single instance of like, update and delete
class LikesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Like.objects.all()
    serializer_class=serializers.LikedSerializer
    permission_classes=[IsOwnerOrReadOnly]
    
    
    # likes count for a post instance
class PostLikesCount(generics.GenericAPIView):
    def get(self, request, post_id, *args, **kwargs):
        try:
            post = models.Post.objects.get(id=post_id)
            likes_count = post.likes.count()
            return Response({"likes_count": likes_count})
        except models.Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)


    # get all likes for a specific post instance
class PostLikesList(generics.ListAPIView):
    serializer_class = serializers.LikedSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return models.Like.objects.filter(post__id=post_id)

    
    # create a new instace of a comment // list all comments*
class ListCreateComments(generics.ListCreateAPIView):
    queryset=models.Comment.objects.all()
    serializer_class=serializers.CommentSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    
    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        serializer.save(owner=user_profile)
        
        
    # retrieve a single instance of a comment , update and delete
class CommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Comment.objects.all()
    serializer_class=serializers.CommentSerializer
    permission_classes=[IsOwnerOrReadOnly]
    
    
    # comments count for a post instance
class PostCommentsCount(generics.GenericAPIView):
    def get(self, request, post_id, *args, **kwargs):
        try:
            post = models.Post.objects.get(id=post_id)
            comments_count = post.comments.count()
            return Response({"comments_count": comments_count})
        except models.Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
    # get all comments for a specific post instance
class PostCommentsList(generics.ListAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return models.Comment.objects.filter(post__id=post_id)

    # create a new bookmark instance // list all bookmarks*
class ListCreateBookmarks(generics.ListCreateAPIView):
    queryset=models.Bookmark.objects.all()
    serializer_class=serializers.BookmarkSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    
    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        serializer.save(owner=user_profile)
     
     
    # retrieve a single instance of a Bookmark , update and delete
class BookmarksDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Bookmark.objects.all()
    serializer_class=serializers.BookmarkSerializer
    permission_classes=[IsOwnerOrReadOnly]
    
    
    # get all bookmarks by a specific user
class UserBookmarksList(generics.ListAPIView):
    serializer_class = serializers.BookmarkSerializer
    parser_classes=[IsAuthenticatedOrReadOnly]

    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user_profile = UserProfile.objects.get(user__id=user_id)
        return models.Bookmark.objects.filter(owner=user_profile)

        # bookmarks count for a post instance
class PostBookmarksCount(generics.GenericAPIView):
    def get(self, request, post_id, *args, **kwargs):
        try:
            post = models.Post.objects.get(id=post_id)
            bookmarks_count = post.bookmarks.count()
            return Response({"bookmarks_count": bookmarks_count})
        except models.Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    # get all bookmarks for a specific post instance
class PostBookmarksList(generics.ListAPIView):
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return models.Bookmark.objects.filter(post__id=post_id)

    
    

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
        )