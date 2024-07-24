from django.urls import path
from . import views

# create your urls here

urlpatterns = [
    path("", views.ListCreateEvents.as_view(), name="event-list"),
    path("<int:pk>/",views.EventDetail.as_view(), name="event-detail"),
    path("me/", views.CurrentUserEventsList.as_view(), name='my-posts-list'),

    
    path("likes/<int:event_id>/",views.CreateLikes.as_view(), name="event-like"),
    path("unlikes/<int:event_id>/",views.UnlikeEvent.as_view(), name="event-unlike"),
    path("likes/event/<int:event_id>/",views.EventLikesList.as_view(), name="event-likes-list"),
    
    path("comments/<int:event_id>/",views.CreateComments.as_view(), name="event-comment"),
    path("uncomments/<int:event_id>/",views.DeleteComment.as_view(), name="event-uncomment"),
    path("comments/event/<int:event_id>/",views.EventCommentsList.as_view(), name="event-comment-list"),
    
    path("bookmarks/<int:event_id>/", views.CreateBookmarks.as_view() , name='bookmark-create'),
    path("unbookmarks/<int:event_id>/", views.UnbookmarkPost.as_view(),name="unbookmark-post"),
    path('bookmarks/user/<int:event_id>/', views.UserBookmarksList.as_view(), name='user-bookmarks-list'),
    path('bookmarks/me/', views.CurrentUserBookmarksList.as_view(), name='my-bookmarks-list'),
    
    path("users/<int:user_id>/", views.SpecificUserList.as_view(), name=""), # List all event posts by a specific user.
    
    path("search/",views.EventSearchView.as_view()),
]
