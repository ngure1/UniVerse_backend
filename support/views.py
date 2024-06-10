from . import models
from . import serializers
from accounts.models import UserProfile
from accounts.pagination import CustomPagination
from rest_framework.exceptions import NotFound
from django.db.models import Q
from .permissions import IsAdminOrReadOnly
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



# Create your views here.
class ListCreateSupport(generics.ListCreateAPIView):
    queryset = models.Support.objects.all().order_by('-created_at')
    serializer_class = serializers.SupportSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination
    
    def perform_create(self, serializer):
        user = self.request.user

        # Ensure the user has a related UserProfile
        try:
            user_profile = user.user_profile
        except UserProfile.DoesNotExist:
            raise NotFound("UserProfile matching query does not exist.")

        # Check if the user is a superuser (admin)
        if not user.is_superuser:
            raise ValidationError(_("Only admins can create announcements."))

        serializer.save(creator=user_profile)


class SupportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Support.objects.all().order_by('-created_at')
    serializer_class = serializers.SupportSerializer
    permission_classes = [IsAdminOrReadOnly]


# class UserSupportsList(generics.ListAPIView):
#     serializer_class = serializers.SupportSerializer
#     permission_classes = [IsAdminOrReadOnly]
#     pagination_class = CustomPagination

#     def get_queryset(self):
#         user_id = self.kwargs.get('user_id')
#         try:
#             user_profile = UserProfile.objects.get(user__id=user_id)
#             supports = models.Support.objects.filter(author=user_profile).order_by('-created_at')  # Adjust the model and field names as needed
#             if not supports.exists():
#                 raise NotFound("This user does not have any support instances.")
#             return supports
#         except UserProfile.DoesNotExist:
#             raise NotFound("User profile does not exist")


# SearchView support
class SupportSearchView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = serializers.SupportSerializer

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q', '')

        if not query:
            return Response({'error': _('Query parameter "q" is required.')}, status=status.HTTP_400_BAD_REQUEST)

        support_results = models.Support.objects.filter(
            Q(title__icontains=query) |
            Q(amount__icontains=query)
        )

        support_serializer = self.get_serializer(support_results, many=True)

        return Response({'supports': support_serializer.data})
