from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SpamEmail, CustomUser
from .utils import is_phishing_email
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from .serializers import UserRegistrationSerializer, CustomLoginSerializer, SpamEmailSerializer, PasswordResetRequestSerializer, PasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework import generics
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


# Get the user model
User = get_user_model()


class SpamDetectionAPIView(APIView):
    def post(self, request):
        emails = request.data.get('emails', [])
        if not isinstance(emails, list):
            return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)

        detected_spam_emails = []
        for email in emails:
            if not isinstance(email, dict):
                return Response({"error": "Invalid email object"}, status=status.HTTP_400_BAD_REQUEST)

            message_id = email.get('messageID', '')
            sender = email.get('from', '')
            subject = email.get('subject', '')
            body = email.get('body', '')

            if is_phishing_email(subject, body, sender):
                spam_email = SpamEmail.objects.create(
                    message_id=message_id,
                    sender=sender,
                    subject=subject,
                    body=body
                )
                detected_spam_emails.append(SpamEmailSerializer(spam_email).data)

        return Response({"spam_emails": detected_spam_emails}, status=status.HTTP_200_OK)


class PhishingRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def get_queryset(self):
        # This view doesn't list users, so return an empty queryset
        return User.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = serializer.save()
        return user


class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'detail': 'Login successful'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'detail': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            reset_link = f"{current_site}/reset/{uid}/{token}/"

            # Send email (you can customize this)
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"detail": "Password reset link sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)



class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user)
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)

        except (User.DoesNotExist, ValueError):
            return Response({"detail": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)
