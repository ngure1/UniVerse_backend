from django.urls import path
from . import views

urlpatterns = [
    path("posts/listcreate/", views.ListCreatePosts.as_view(), name='post-list-create'),
    path("posts/detail/<int:pk>/", views.PostsDetail.as_view(),name="post-detail"),
    path('posts/user/<int:user_id>/', views.UserPostsList.as_view(), name='user-posts-list'),
    
    path("likes/create/", views.CreateLikes.as_view()),
    path("likes/detail/<int:pk>/", views.LikesDetail.as_view(),name="like-detail"),
    path('likes/count/<int:post_id>/', views.PostLikesCount.as_view(), name='post-likes-count'),
    path('likes/list/<int:post_id>/', views.PostLikesList.as_view(), name='post-likes-list'),
    
    path("comments/create/", views.CreateComments.as_view()),
    path("comments/detail/<int:pk>/", views.CommentsDetail.as_view(),name="comment-detail"),
    path('comments/count/<int:post_id>/', views.PostCommentsCount.as_view(), name='post-comments-count'),
    path('comments/list/<int:post_id>/', views.PostCommentsList.as_view(), name='post-comments-list'),
    
    path("bookmarks/create/", views.CreateBookmarks.as_view()),
    path("bookmarks/detail/<int:pk>/", views.BookmarksDetail.as_view(),name="bookmark-detail"),
    path('bookmarks/count/<int:post_id>/', views.PostBookmarksCount.as_view(), name='post-bookmarks-count'),
    path('bookmarks/list/<int:post_id>/', views.PostBookmarksList.as_view(), name='post-bookmarks-list'),
    path('bookmarks/user/<int:user_id>/', views.UserBookmarksList.as_view(), name='user-bookmarks-list'),

    path("search/", views.SearchPosts.as_view()),
]