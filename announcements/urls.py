from django.urls import path
from . import views
from . import models


#urlpatterns for Announcements app
urlpatterns = [
    path("list/", views.ListCreateAnnouncement.as_view()),
    path("detail/<int:pk>/", views.AnnouncementDetail.as_view()),
    path("search/", views.search_announcements)
]
