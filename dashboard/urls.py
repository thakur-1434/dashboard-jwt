
from django.urls import path
from django.contrib import admin
from dashboard.views import UserRegistrationView,UserLoginView,LogoutView, UserProfileView, HomeView, AboutView,TokenRefreshCookieView, ContactView,all_users_view,search_users

urlpatterns = [
    path('', HomeView.as_view(), name='home'), 
    path('about/', AboutView.as_view(), name='about'), 
    path('contact/', ContactView.as_view(), name='contact'),
    path('search/', search_users, name='search'), 
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('allusers/', all_users_view, name='all_users'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('token/refresh/', TokenRefreshCookieView.as_view(), name='token_refresh'),
]