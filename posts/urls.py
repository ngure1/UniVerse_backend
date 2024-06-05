from django.urls import path
from . import views
from . import models
urlpatterns = [
    path("list/", views.ListCreatePosts.as_view()),
    path("detail/<int:pk>/", views.PostsDetail.as_view(),name="post-detail"),
    path('user/<int:user_id>/posts/', views.UserPostsList.as_view(), name='user-posts-list'),
    path('<int:post_id>/comments/count/', views.PostCommentsCount.as_view(), name='post-comments-count'),
    path('<int:post_id>/comments/', views.PostCommentsList.as_view(), name='post-comments-list'),
    path('<int:post_id>/likes/count/', views.PostLikesCount.as_view(), name='post-likes-count'),
    path('<int:post_id>/likes/', views.PostLikesList.as_view(), name='post-likes-list'),
    path('<int:post_id>/bookmarks/count/', views.PostBookmarksCount.as_view(), name='post-bookmarks-count'),
    path('<int:post_id>/bookmarks/', views.PostBookmarksList.as_view(), name='post-bookmarks-list'),

    path("search/", views.SearchPosts.as_view()),
]