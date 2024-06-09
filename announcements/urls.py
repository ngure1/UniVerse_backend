from django.urls import path
from . import views
from . import models


#urlpatterns for Announcements app
urlpatterns = [
    path("listcreate/", views.ListCreateAnnouncement.as_view()),
    path("detail/<int:pk>/", views.AnnouncementDetail.as_view(), name="announcement-detail"),
    path("search/", views.AnnouncementSearchView.as_view())
]
