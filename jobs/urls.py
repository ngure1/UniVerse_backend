from django.urls import path
from . import views
from . import models


urlpatterns = [
    path("list/", views.ListCreateJob.as_view()),
    path("detail/<int:pk>/", views.JobDetail.as_view()),
    path("search/", views.search_jobs),
]