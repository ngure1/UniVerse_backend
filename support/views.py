from . import models
from . import serializers
from django.db.models import Q
from django.shortcuts import render
from .permissions import IsAdminOrReadOnly
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError


# Create your views here.
class ListCreateSupport(generics.ListCreateAPIView):
    queryset = models.Support.objects.all()
    serializer_class = serializers.SupportSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        if not self.request.user.is_superuser:
            raise ValidationError("Only admins can create support posts.")
        serializer.save(owner=user_profile)


class SupportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Support.objects.all()
    serializer_class = serializers.SupportSerializer
    permission_classes = [IsAdminOrReadOnly]


# SearchView support
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def search_support(request):
    query = request.GET.get('q', '')

    if not query:
        return Response({'error': 'Query parameter "q" is required.'}, status=status.HTTP_400_BAD_REQUEST)

    support_results = models.Support.objects.filter(
        Q(title__icontains=query) | 
        Q(amount__icontains=query)
    )

    support_serializer = serializers.SupportSerializer(support_results, many=True)

    return Response({
        'supports': support_serializer.data
    })
