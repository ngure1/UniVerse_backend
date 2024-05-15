from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

# custom jwt authentication class
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            # Get the JWT token from the request header or cookies
            header = self.get_header(request)

            if header is None:
                # If the header is None, try to get the token from cookies
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
            else:
                # If the header is present, get the raw token
                raw_token = self.get_raw_token(header)

            if raw_token is None:
                # If the token is None, return None
                return None

            # Validate the token and get the validated token
            validated_token = self.get_validated_token(raw_token)

            # Get the user associated with the validated token
            user = self.get_user(validated_token)

            # Return the user and the validated token
            return user, validated_token
        except:
            # If any exception occurs, return None
            return None