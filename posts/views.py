from . import models
from . import serializers
from rest_framework.request import Request
from rest_framework import generics
from rest_framework.decorators import APIView


class ListCreatePosts(generics.ListCreateAPIView):
    queryset=models.Post.objects.all()
    serializer_class=serializers.PostSerializer

class PostsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=models.Post.objects.all()
    serializer_class=serializers.PostSerializer
    