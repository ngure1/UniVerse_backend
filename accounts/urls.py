
from django.urls import path, re_path,include
from .views import (CustomProviderAuthView,
                    CustomTokenObtainPairView,
                    CustomTokenRefreshView,
                    CustomTokenVerifyView,
                    LogoutView,
                    ListProfile,
                    ProfileDetail,
                    search,
                    FollowToggleView,
                    FollowerList,
                    FollowingList,
                    )

urlpatterns = [
    # Include the URLs from the 'djoser' app
    path('auth/', include('djoser.urls')),
    re_path(r'^o/(?P<provider>\S+)/$', CustomProviderAuthView.as_view(), name='provider-auth'),
    # Custom JWT token endpoints
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view()),  # Endpoint to obtain JWT token pair
    path('auth/jwt/refresh/', CustomTokenRefreshView.as_view()),  # Endpoint to refresh JWT token
    path('auth/jwt/verify/', CustomTokenVerifyView.as_view()),  # Endpoint to verify JWT token
  
    # Logout endpoint
    path('auth/logout/', LogoutView.as_view()),  # Endpoint to log out user
    path('profilelist/', ListProfile.as_view()),
    path("profiledetail/<int:pk>/", ProfileDetail.as_view()),
    path('Addresslist/', ListProfile.as_view()),
    path("Addressdetail/<int:pk>/", ProfileDetail.as_view()),
    path('Educationlist/', ListProfile.as_view()),
    path("Educationdetail/<int:pk>/", ProfileDetail.as_view()),
    path('accounts/search/', search ),
    path('follow-toggle/', FollowToggleView.as_view()),
    path('followers/', FollowerList.as_view()),
    path('following/', FollowingList.as_view()),

]