from .models import MyUser, UserProfile, Education, Address
from .serializers import MyUserSerializer, UserProfileSerializer, AddressSerializer, EducationSerializer
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
class CustomProviderAuthView(ProviderAuthView):
    def get(self, request, *args, **kwargs):
        provider = kwargs.get('provider')
        if not provider:
            raise ValidationError("Provider parameter is missing in the URL.")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

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