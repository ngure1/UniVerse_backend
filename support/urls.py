from django.urls import path
from . import views


urlpatterns = [
    path("", views.ListCreateSupport.as_view()),
    path("detail/<int:pk>/", views.SupportDetail.as_view(), name="support-detail"),
    path("search/", views.SupportSearchView.as_view()),
]