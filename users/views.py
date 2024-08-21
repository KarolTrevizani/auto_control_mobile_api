from django.contrib.auth import get_user_model, update_session_auth_hash

from django.core.mail import send_mail

from rest_framework import viewsets, status, permissions

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.response import Response

from rest_framework.views import APIView

from .serializers import (
    UserSerializer, CustomAuthTokenSerializer, CreateUserSerializer, ChangePasswordSerializer
    )

from .models import (
    PasswordResetToken
)

from auto_control.settings.base import env

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Manages user CRUD operations. Selects serializers based on action; `CreateUserSerializer` for creation,
    `UserSerializer` for other actions.
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        else:
            return UserSerializer

    def create(self, request, *args, **kwargs):
        if User.objects.filter(email=request.data.get('email')).exists():
            return Response({"detail": "E-mail already registered."}, status=309)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomAuthToken(ObtainAuthToken):
    """
    Authenticates users and returns a token along with user details for valid credentials.
    """

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'user_name': user.name,
            'user_cnh': user.cnh
        })
        

class ChangePasswordView(APIView):
    """
    Enables authenticated users to change their password securely and updates the user session.
    """

    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.data.get("new_password"))
            user.save()
            # Keep the user logged in after changing the password
            update_session_auth_hash(request, user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class RequestPasswordResetEmail(APIView):
    """
    Sends a password reset email with a token if the provided email is associated with an account.
    """
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            reset_token = PasswordResetToken.objects.create(user=user)
            
            send_mail(
                'Reset Your Password',
                f'Use this token to reset your password: {reset_token.token}\nYour link: {env("URL_SITE_RESET_PASSWORD")}/reset-password?token={reset_token.token}',
                env('EMAIL_HOST_USER'),
                [email],
                fail_silently=False,
            )
        return Response({"message": "If an account with this email was found, we have sent an email with instructions to reset your password."}, status=status.HTTP_200_OK)


class ResetPassword(APIView):
    """
    Allows users to reset their password using a valid, non-expired token.
    """
    permission_classes = []
    
    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('password')
        reset_token = PasswordResetToken.objects.filter(token=token, is_used=False).first()
        if reset_token and not reset_token.is_expired():
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            reset_token.is_used = True
            reset_token.save()
            return Response({"message": "Your password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)