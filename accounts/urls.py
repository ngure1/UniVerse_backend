from django.urls import path, include

from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView
)

urlpatterns = [
    # Include the URLs from the 'djoser' app
    path('', include('djoser.urls')),
    
    # Custom JWT token endpoints
    path('jwt/create/', CustomTokenObtainPairView.as_view()),  # Endpoint to obtain JWT token pair
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),  # Endpoint to refresh JWT token
    path('jwt/verify/', CustomTokenVerifyView.as_view()),  # Endpoint to verify JWT token
    
    # Logout endpoint
    path('logout/', LogoutView.as_view()),  # Endpoint to log out user
]