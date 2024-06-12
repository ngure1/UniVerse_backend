from rest_framework.exceptions import APIException
from rest_framework import status


class UserProfileDoesNotExist(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User profile does not exist for this user."
    default_code = "user_profile_not_found"
