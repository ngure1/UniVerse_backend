
from django.urls import path, re_path,include
from .views import (CustomProviderAuthView,
                    CustomTokenObtainPairView,
                    CustomTokenRefreshView,
                    CustomTokenVerifyView,
                    LogoutView,
                    ListProfile,
                    ProfileDetail,
                    SearchView,
                    FollowToggleView,
                    FollowerList,
                    FollowingList,

                    UserProfileDetail,
                    UserAddressDetail,
                    UserEducationDetail,

                    AddressProfile,
                    AddressDetail,
                    EducationProfile,
                    EducationDetail
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
    path('Educationlist/', ListProfile.as_view()),
    path('accounts/search/', SearchView.as_view() ),
    path('follow-toggle/', FollowToggleView.as_view()),
    path('followers/', FollowerList.as_view()),
    path('following/', FollowingList.as_view()),

        # LoggedInUser URLs
    path('profile/<int:pk>/', ProfileDetail.as_view()),  # View and update the logged-in user's profile
    path('address/create/', AddressProfile.as_view()),  # Create and list addresses for the logged-in user
    path('address/<int:pk>/', AddressDetail.as_view()),  # Retrieve, update, or delete a specific address for the logged-in user
    path('education/create/', EducationProfile.as_view()),  # Create and list education details for the logged-in user
    path('education/<int:pk>/', EducationDetail.as_view()),  # Retrieve, update, or delete a specific education detail for the logged-in user
    
    # Normal User URLs
    path('user/profile/<int:pk>/', UserProfileDetail.as_view(), name="userprofile-detail"),  # View the profile of a normal user
    path('user/address/<int:pk>/', UserAddressDetail.as_view()),  # View the addresses of a normal user
    path('user/education/<int:pk>/', UserEducationDetail.as_view()),  # View the education details of a normal user


]