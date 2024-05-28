from django.urls import path
from . import views
from . import models
urlpatterns = [
    path("list/", views.ListCreatePosts.as_view()),
    path("detail/<int:pk>/", views.PostsDetail.as_view()),
    path('user/<int:user_id>/posts/', views.UserPostsList.as_view(), name='user-posts-list'),
    # path("posts/", views.postList),
    # path("posts/<int:pk>/", views.postDetail),
    path("search/", views.search_posts),
]