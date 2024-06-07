from django.shortcuts import render
from .models import Event
from .serializers import EventSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from posts.permissions import IsOwnerOrReadOnly
from accounts.models import UserProfile
from django.db.models import Q
from support.permissions import IsAdminOrReadOnly
from django.utils.translation import gettext_lazy as _ 


# Create your views here.


class ListCreateEVent(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self,serializer):
        user_profile = UserProfile.objects.get(user=self.request.user)
        serializer.save(creator=user_profile)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()  
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class EventSearchView(generics.GenericAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        query = self.request.GET.egt('q','')

        if not query:
            return Response({'error': _('Query parameter "q" is required.')}, status=status.HTTP_400_BAD_REQUEST)

        event_results = Event.Objects.filter(
            Q(title__icontains=query) |
            Q(creator__user_email__icontains=query) |
            Q(creator__user__first_name__icontains=query) |
            Q(description__icontains=query) |
            Q(address__street__icontains=query) |  
            Q(address__city__icontains=query)

        )


        event_serializer = self.get_serializer(event_results, many=True)

        return Response({'Events' : event_serializer.data})







