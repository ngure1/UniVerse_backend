from django.urls import path, re_path,include
from .views import (CustomProviderAuthView,
                    CustomTokenObtainPairView,
                    CustomTokenRefreshView,
                    CustomTokenVerifyView,
                    LogoutView
                    )

urlpatterns = [
    # Include the URLs from the 'djoser' app
    path('', include('djoser.urls')),
    re_path(r'^o/(?P<provider>\S+)/$', CustomProviderAuthView.as_view(), name='provider-auth'),
    # Custom JWT token endpoints
    path('jwt/create/', CustomTokenObtainPairView.as_view()),  # Endpoint to obtain JWT token pair
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),  # Endpoint to refresh JWT token
    path('jwt/verify/', CustomTokenVerifyView.as_view()),  # Endpoint to verify JWT token
    
    # Logout endpoint
    path('logout/', LogoutView.as_view()),  # Endpoint to log out user
]