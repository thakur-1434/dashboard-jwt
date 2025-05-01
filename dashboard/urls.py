
from django.urls import path
from django.contrib import admin
from dashboard.views import UserRegistrationView,UserLoginView,LogoutView, UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('logout/', LogoutView.as_view(),name='logout'),

]
