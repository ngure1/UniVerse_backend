from django.urls import path
from . import models
from . import views

# create your urls here

urlpatterns = [
    path("listcreate/",views.ListCreateEvent.as_view()),
    path("detail/<int:pk>/",views.EventDetail.as_view(), name="event-detail"),
    path("search/",views.EventSearchView.as_view()),
    path('user/<int:user_id>/', views.UserEventsList.as_view(), name='user-events-list'),
]
