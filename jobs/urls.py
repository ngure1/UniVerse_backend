from django.urls import path
from . import views


urlpatterns = [
   path("", views.ListCreateJob.as_view(), name="job-list-create"),
   path("detail/<int:pk>/", views.JobDetail.as_view(), name="job-detail"),
  
  
   # Bookmarking
   path("bookmarks/<int:job_id>/", views.CreateBookmarks.as_view(), name='bookmark-create'),
   path("unbookmarks/<int:job_id>/", views.UnbookmarkJob.as_view(), name="unbookmark-job"),
  
   # for currently logged in user
   path('jobs/me/', views.CurrentUserJobsList.as_view(), name='current-user-jobs-list'),  # List jobs for the current user
   path('bookmarks/me/', views.CurrentUserJobBookmarksList.as_view(), name='my-job-bookmarks-list'), # Current Logged In user
  
   # for specific user
   path('jobs/user/<int:user_id>/', views.UserJobsList.as_view(), name='user-jobs-list'), # Lists all Jobs for Specific
   path('bookmarks/user/<int:user_id>/', views.UserJobBookmarksList.as_view(), name='user-bookmarks-list'),
  
   # Search View
   path("search/", views.JobSearchView.as_view(), name="job-search"),
]

