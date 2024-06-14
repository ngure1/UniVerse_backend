from django.http import Http404
from .models import UserProfile, Education, Address, Follower
from .serializers import UserProfileSerializer, AddressSerializer, EducationSerializer, FollowerSerializer
from django.conf import settings
from rest_framework import status,generics,views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated 
from django.db.models import Q
from rest_framework.throttling import UserRateThrottle
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .pagination import CustomPagination
import logging
from posts.permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404


class CustomProviderAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        # Call the parent class's post method
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            # Get the access and refresh tokens from the response data
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            # Set cookies for the access and refresh tokens
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining token pairs (access and refresh tokens).
    Inherits from TokenObtainPairView.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the POST request to obtain token pairs.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response object.

        """
        # Call the parent class's post method
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Get the access and refresh tokens from the response data
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            # Set cookies for the access and refresh tokens
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Get the refresh token from the cookies
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            # Set the refresh token in the request data
            request.data['refresh'] = refresh_token

        # Call the parent class's post method
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Get the new access token from the response data
            access_token = response.data.get('access')

            # Set the new access token in the response cookies
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        # Get the access token from the cookies
        access_token = request.COOKIES.get('access')

        if access_token:
            # Set the access token in the request data
            request.data['token'] = access_token

        # Call the parent class's post method
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        # Create a response with status code 204 (No Content)
        response = Response(status=status.HTTP_204_NO_CONTENT)

        # Delete the access and refresh cookies from the response
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response

# LoggedInUser      
class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        user = self.request.user
        try:
            return user.user_profile
        except UserProfile.DoesNotExist:
            raise Http404("UserProfile does not exist for this user.")

class AddressProfile(generics.CreateAPIView):
    queryset=Address.objects.all()
    serializer_class=AddressSerializer
    permission_classes=[IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        user_profile = self.request.user.user_profile
        if hasattr(user_profile, 'address') and user_profile.address is not None:
            raise ValidationError({"detail" : "This user already has an address associated."})
        address = serializer.save()
        user_profile.address = address
        user_profile.save()
        
        
class AddressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Address.objects.all()
    serializer_class=AddressSerializer
    permission_classes=[IsOwnerOrReadOnly]

    def get_queryset(self):
        return Address.objects.filter(profile_address=self.request.user.user_profile)

class EducationProfile(generics.ListCreateAPIView):
    queryset=Education.objects.all().order_by('-created_at')
    serializer_class=EducationSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    pagination_class=CustomPagination

    def get_queryset(self):
        return Education.objects.filter(owner=self.request.user.user_profile)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.user_profile)
        
class EducationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Education.objects.all()
    serializer_class=EducationSerializer
    permission_classes=[IsOwnerOrReadOnly]

    def get_queryset(self):
        return Education.objects.filter(owner=self.request.user.user_profile)


# Normal User
class UserProfileDetail(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserAddressDetail(generics.RetrieveAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserEducationDetail(generics.RetrieveAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    
class SearchView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return UserProfileSerializer  # Default serializer class, not used directly

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q', '')

        if not query:
            return Response({'error': 'Query parameter "q" is required.'}, status=400)

        user_profiles = UserProfile.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query)
        )
        education_results = Education.objects.filter(
            Q(institution_name__icontains=query) | 
            Q(field_of_study__icontains=query)
        )
        address_results = Address.objects.filter(
            Q(street__icontains=query) | 
            Q(city__icontains=query) | 
            Q(country__icontains=query)
        )

        profile_serializer = UserProfileSerializer(user_profiles, many=True)
        education_serializer = EducationSerializer(education_results, many=True)
        address_serializer = AddressSerializer(address_results, many=True)

        combined_results = {
            'user_profile': profile_serializer.data,
            'education': education_serializer.data,
            'address': address_serializer.data
        }

        return Response(combined_results)


logger = logging.getLogger(__name__)

class FollowThrottle(UserRateThrottle):
    rate = '5/min'

class FollowToggleView(views.APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [FollowThrottle]

    def post(self, request, *args, **kwargs):
        follower = request.user.user_profile
        followed_id = request.data.get('followed_id')

        if not followed_id:
            return Response({'error': 'followed_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if follower.id == followed_id:
            return Response({'error': "Users cannot follow themselves."}, status=status.HTTP_400_BAD_REQUEST)
        
        followed = get_object_or_404(UserProfile, id=followed_id)

        follow_relation, created = Follower.objects.get_or_create(follower=follower, followed=followed)
        
        if not created:
            follow_relation.delete()
            logger.info(f"User {follower.user.email} unfollowed {followed.user.email}")
            return Response({'message': "Unfollowed successfully."}, status=status.HTTP_200_OK)

        logger.info(f"User {follower.user.email} followed {followed.user.email}")
        return Response({'message': "Followed successfully."}, status=status.HTTP_201_CREATED)

@method_decorator(cache_page(60*2), name='dispatch')  # Cache the view for 2 minutes
class FollowerList(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return Follower.objects.filter(followed=user_profile)

@method_decorator(cache_page(60*2), name='dispatch')  # Cache the view for 2 minutes
class FollowingList(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        return Follower.objects.filter(follower=user_profile)
