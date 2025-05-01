from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from dashboard.renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken,TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from dashboard.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer


# genetate token 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# registration View
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format = None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'message':'register successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#login View
class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request, format = None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'message':'Login Sucess'},status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not Valid']}},status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# user profile view
class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self, request, format =None):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

#logout view
class LogoutView(APIView):
    renderer_classes=[UserRenderer] 
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        except (TokenError, InvalidToken):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)