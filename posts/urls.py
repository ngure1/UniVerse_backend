from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListCreatePosts.as_view(), name='post-list-create'),
    path("<int:pk>/", views.PostsDetail.as_view(),name="post-detail"),
    path('user/<int:user_id>/', views.UserPostsList.as_view(), name='user-posts-list'),
    path("me/", views.CurrentUserPostsList.as_view(), name='my-posts-list'),
    
    path("likes/<int:post_id>/", views.CreateLikes.as_view() , name='like-create'),
    path('unlikes/<int:post_id>/', views.UnlikePost.as_view(), name='post-unlike'),
    path('likes/post/<int:post_id>/', views.PostLikesList.as_view(), name='post-likes-list'),
    
    path("comments/<int:post_id>/", views.CreateComments.as_view() , name='comment-create'),
    path("uncomments/<int:post_id>/", views.DeleteComment.as_view(),name="comment-detail"),
    path('comments/post/<int:post_id>/', views.PostCommentsList.as_view(), name='post-comments-list'),
    
    path("bookmarks/<int:post_id>/", views.CreateBookmarks.as_view() , name='bookmark-create'),
    path("unbookmarks/<int:post_id>/", views.UnbookmarkPost.as_view(),name="unbookmark-post"),
    path('bookmarks/user/<int:user_id>/', views.UserBookmarksList.as_view(), name='user-bookmarks-list'),
    path('bookmarks/me/', views.CurrentUserBookmarksList.as_view(), name='my-bookmarks-list'),

    path("search/", views.SearchPosts.as_view() , name='post-search'),
]