from django.urls import path
from . import views
urlpatterns = [
    path("list", views.ListCreatePosts.as_view()),
    path("detail", views.PostsDetail.as_view())
]
