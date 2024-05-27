from . import models
from . import serializers
# from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
# from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from accounts.models import UserProfile


class ListCreatePosts(generics.ListCreateAPIView):
    queryset=models.Post.objects.all()
    serializer_class=serializers.PostSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        serializer.save(author=user_profile)
        
class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Post.objects.all()
    serializer_class=serializers.PostSerializer
    permission_classes=[IsOwnerOrReadOnly]
    
    
class ListCreateLikes(generics.ListCreateAPIView):
    queryset=models.Like.objects.all()
    serializer_class=serializers.LikedSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        serializer.save(owner=user_profile)
    
class LikesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Like.objects.all()
    serializer_class=serializers.LikedSerializer
    permission_classes=[IsOwnerOrReadOnly]
    
    
class ListCreateComments(generics.ListCreateAPIView):
    queryset=models.Comment.objects.all()
    serializer_class=serializers.CommentSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        serializer.save(owner=user_profile)
        
class CommentsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Comment.objects.all()
    serializer_class=serializers.CommentSerializer
    permission_classes=[IsOwnerOrReadOnly]
    
    
class ListCreateBookmarks(generics.ListCreateAPIView):
    queryset=models.Bookmark.objects.all()
    serializer_class=serializers.BookmarkSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        serializer.save(owner=user_profile)
        
class BookmarksDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Bookmark.objects.all()
    serializer_class=serializers.BookmarkSerializer
    permission_classes=[IsOwnerOrReadOnly]
    
   #  get all posts by a user
class UserPostsList(generics.ListAPIView):
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user_profile = UserProfile.objects.get(user__id=user_id)
        return models.Post.objects.filter(author=user_profile)
    
    # get all bookmarks by a user
class UserBookmarksList(generics.ListAPIView):
    serializer_class = serializers.BookmarkSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user_profile = UserProfile.objects.get(user__id=user_id)
        return models.Bookmark.objects.filter(owner=user_profile)
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# @api_view(["GET", "POST"])
# def postList(request):
#     if request.method=="GET":
#         posts=models.Post.objects.all()
#         serializer=serializers.PostSerializer(posts)
#         return Response(serializer.data)
    
#     elif request.method=="POST":
#         serializer=serializers.PostSerializer(data=request.data)
#         if serializer.is_valid:
#             serializer.save()
#             return Response(serializer.data, status.HTTP_201_CREATED)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    

# @api_view(["GET", "PUT", "PATCH", "DELETE"])
# def postDetail(request, pk):
#     try:
#         post=models.Post.objects.get(pk=pk)
        
#     except post.DOESNOTEXIST:
#         return Response(status.HTTP_404_NOT_FOUND)
    
#     if request.method=="GET":
#         serializer=serializers.PostSerializer(post)
#         return Response(serializer.data)

#     elif request.method=="PATCH":
#         serializer= serializers.PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(status.HTTP_400_BAD_REQUEST)
    
#     elif request.method=="DELETE":
#         post.delete()
#         return Response(status.HTTP_204_NO_CONTENT)