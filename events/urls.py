from django.urls import path
from . import models 
from . import views

# create your urls here 
urlpatterns = [
    path("list/",views.ListCreateEVent.as_view()),
    path("detail/<int:pk>/",views.EventDetail.as_view()),
    path("search/",views.EventSearchView.as_view())
]
