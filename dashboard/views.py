from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from dashboard.renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from dashboard.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.safestring import mark_safe
from dashboard.models import User

# Helper function to generate access and refresh tokens for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# ------------------ Static Page Views ------------------

# Renders the home page
class HomeView(APIView):
    def get(self, request, format=None):
        return render(request, 'home.html')

# Renders the about page
class AboutView(APIView):
    def get(self, request, format=None):
        return render(request, 'about.html')

# Renders the contact page
class ContactView(APIView):
    def get(self, request, format=None):
        return render(request, 'contact.html')


# ------------------ User Registration ------------------

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, format=None):
        return render(request, 'home.html') 
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            # Show success message and token
            message = mark_safe(f"Your account has been successfully created.<br>Token: {token['access']}")
            messages.success(request, message)
            return redirect('home')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------ User Login ------------------

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def get(self, request, format=None):
        return render(request, 'register.html')
    def post(self, request, format=None):
        email = request.POST.get('email')
        password = request.POST.get('password')
        serializer = UserLoginSerializer(data={'email': email, 'password': password})

        if serializer.is_valid():
            user = authenticate(request, email=email, password=password)
            if user is not None:
                tokens = get_tokens_for_user(user)
                response = redirect('profile') 
                # Set tokens in HTTP-only cookies
                response.set_cookie('access_token', tokens['access'], httponly=True, samesite='Lax')
                response.set_cookie('refresh_token', tokens['refresh'], httponly=True, samesite='Lax')
                messages.success(request, "Successfully logged in.")
                return response
            else:
                return render(request, 'login.html', {'login_error': 'Invalid email or password'})

        return render(request, 'login.html', {'login_error': serializer.errors})


# ------------------ User Profile ------------------

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user)
        return render(request, 'profile.html', {'user_data': serializer.data})


# ------------------ User Logout ------------------

class LogoutView(APIView):
    def post(self, request):
        # Clear JWT cookies and redirect to home
        response = redirect('home')
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        messages.success(request, "Successfully logged out.")
        return response


# ------------------ Refresh Token via Cookie ------------------

class TokenRefreshCookieView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({'error': 'Refresh token not provided'}, status=400)

        try:
            # Decode refresh token and generate a new access token
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)

            response = Response({'access': access_token})
            response.set_cookie('access_token', access_token, httponly=True, samesite='Lax')
            return response
        except TokenError:
            return Response({'error': 'Invalid or expired refresh token'}, status=400)
