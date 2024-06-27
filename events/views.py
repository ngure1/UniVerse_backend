from . import models
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .import serializers
from .mixins import GetUserProfileAndEventMixin
from posts.permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import NotFound
from accounts.pagination import CustomPagination
from rest_framework.response import Response
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

    # list all events* // create a new event
class ListCreateEvents(generics.ListCreateAPIView, GetUserProfileAndEventMixin):
    queryset = models.Event.objects.all().order_by('-created_at')
    serializer_class = serializers.EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    
    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        serializer.save(author=user_profile)

    # retrieve a single instance of event, update and delete
class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Event.objects.all().order_by('-created_at')
    serializer_class = serializers.EventSerializer
    permission_classes = [IsOwnerOrReadOnly]

    
    
    # get all likes for a specific event
class CreateLikes(generics.CreateAPIView, GetUserProfileAndEventMixin):
    queryset = models.Like.objects.all().order_by('-created_at')
    serializer_class = serializers.LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        event = self.get_event()
        if models.Like.objects.filter(event=event, author=user_profile).exists():
            raise NotFound("You have already liked this event.")
        serializer.save(author=user_profile, event=event)
        
        
        #unlike an event
class UnlikeEvent(generics.GenericAPIView, GetUserProfileAndEventMixin):
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    def delete(self, request, *args, **kwargs):
        user_profile = self.get_user_profile()
        event = self.get_event()
        
        try:
            like = models.Like.objects.get(event=event, author=user_profile)
            like.delete()
            return Response({"detail": "You have unliked this event."}, status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:
            return Response({"detail": "You have not liked this event."}, status=status.HTTP_400_BAD_REQUEST)


class EventLikesList(generics.ListAPIView, GetUserProfileAndEventMixin):
    serializer_class = serializers.LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        event = self.get_event()
        return models.Like.objects.filter(event=event).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "This event has no likes."}, status=status.HTTP_204_NO_CONTENT)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    # comment on an event
class CreateComments(generics.CreateAPIView, GetUserProfileAndEventMixin):
    queryset = models.Comment.objects.all().order_by('-created_at')
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        event = self.get_event()
        
        if models.Comment.objects.filter(event=event, author=user_profile).exists():
            raise NotFound("You have already commented on this event.")
        
        serializer.save(author=user_profile, event=event)
        
        # delete a comment
class DeleteComment(generics.GenericAPIView, GetUserProfileAndEventMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, post_id, *args, **kwargs):
        
        user_profile = self.get_user_profile()
        event = self.get_event()

        try:
            comment = models.Comment.objects.get(event=event, author=user_profile)
            comment.delete()
            return Response({"detail": "Deleted the comment successfully."}, status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response({"detail": "Comment does not exist or you are not the author of the comment."}, status=status.HTTP_400_BAD_REQUEST)
        
class EventCommentsList(generics.ListAPIView, GetUserProfileAndEventMixin):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        event = self.get_event()
        return models.Comment.objects.filter(event=event).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "This event has no comments."}, status=status.HTTP_204_NO_CONTENT)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    # bookmark an event
class CreateBookmarks(generics.CreateAPIView, GetUserProfileAndEventMixin):
    queryset = models.Bookmark.objects.all().order_by('-created_at')
    serializer_class = serializers.BookmarkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user_profile = self.get_user_profile()
        event = self.get_event()
        
        if models.Bookmark.objects.filter(event=event, author=user_profile).exists():
            raise NotFound("You have already bookmarked this event.")
        
        serializer.save(author=user_profile, event=event)
        
            # unbookmark an event
class UnbookmarkPost(generics.GenericAPIView, GetUserProfileAndEventMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request,*args, **kwargs):
        
        user_profile = self.get_user_profile()
        event = self.get_event()


        try:
            bookmark = models.Bookmark.objects.get(event=event, author=user_profile)
            bookmark.delete()
            return Response({"detail": "Unbookmarked the event successfully."}, status=status.HTTP_204_NO_CONTENT)
        except models.Bookmark.DoesNotExist:
            return Response({"detail": "Bookmark does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
      # get all bookmarks by a specific user
class UserBookmarksList(generics.ListAPIView, GetUserProfileAndEventMixin):
    serializer_class = serializers.EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if not user_id:
            raise NotFound("User ID not provided.")
        user_profile = self.get_user_profile_by_id(user_id)
        bookmarked_posts = models.Event.objects.filter(event_bookmarks__author=user_profile).order_by('-created_at') # get all posts that have been bookmarked by this user
        if not bookmarked_posts.exists():
            raise NotFound("This user does not have any bookmarked posts.")
        return bookmarked_posts
    
    
    # get all bookmarks by the current logged in  user
class CurrentUserBookmarksList(generics.ListAPIView, GetUserProfileAndEventMixin):
    serializer_class = serializers.EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_profile = self.get_user_profile()
        bookmarked_posts = models.Event.objects.filter(event_bookmarks__author=user_profile).order_by('-created_at') # get all posts that have been bookmarked by this user
        return bookmarked_posts

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class EventSearchView(generics.GenericAPIView):
    serializer_class = serializers.EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q', '')

        if not query:
            return Response({'error': _('Query parameter "q" is required.')}, status=status.HTTP_400_BAD_REQUEST)

        event_results = models.Event.objects.filter(
            Q(title__icontains=query) |
            Q(author__user__email__icontains=query) |
            Q(author__user__first_name__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-created_at')

        event_serializer = self.get_serializer(event_results, many=True)
        return Response({'Events': event_serializer.data})




    # get all events by a specific user
# class UserEventsList(generics.ListAPIView):
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         user_id = self.kwargs.get('user_id')
#         try:
#             user_profile = UserProfile.objects.get(user__id=user_id)
#             events=Event.objects.filter(author=user_profile)
#             if not events.exists():
#                 raise NotFound("This user does not have any event postings.")
#         except UserProfile.DoesNotExist:
#             raise NotFound("User profile does not exist")




    # get all events created by the current user
# class CurrentUserEventsList(generics.ListAPIView, GetUserProfileAndEventMixin):
#     serializer_class = serializers.EventSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         user_profile = self.get_user_profile()
#         return models.Event.objects.filter(author=user_profile).order_by('-created_at')
    
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         if not queryset.exists():
#             return Response({"detail": "The current user has no events."}, status=status.HTTP_204_NO_CONTENT)
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)