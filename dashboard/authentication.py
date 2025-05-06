from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()


# Custom Authentication Backend for Email-based Login
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Allow login using email 
        email = username or kwargs.get('email')
        try:
            # Try to fetch user by email
            user = User.objects.get(email=email)
            # Check password and if the user is active
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            # Return None if no matching user is found
            return None


# Custom JWT Authentication Class to read token from cookies
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get JWT token from browser cookie named 'access_token'
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            # No token found in cookies
            return None
        try:
            # Validate the token using SimpleJWT
            validated_token = self.get_validated_token(raw_token)
            # Return the associated user and the validated token
            return self.get_user(validated_token), validated_token
        except Exception:
            # Return None if token is invalid or user not found
            return None
