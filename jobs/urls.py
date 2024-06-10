from django.urls import path
from . import views
from . import models


urlpatterns = [
    path("list/", views.ListCreateJob.as_view()),
    path("detail/<int:pk>/", views.JobDetail.as_view(), name="job-detail"),
    path("search/", views.JobSearchView.as_view()),
    path('jobs/user/<int:user_id>/', views.UserJobsList.as_view(), name='user-jobs-list'),
]