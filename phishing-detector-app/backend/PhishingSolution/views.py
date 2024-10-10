from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SpamEmail, CustomUser
from .utils import is_phishing_email
from rest_framework import permissions
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from .serializers import UserRegistrationSerializer, CustomLoginSerializer, SpamEmailSerializer
from django.contrib.auth import authenticate
from rest_framework import generics
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user = serializer.save()
        return user


class CustomLoginView(APIView):
    serializer_class = CustomLoginSerializer
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


class CustomLogoutView(LogoutView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.data['detail'] = 'Logout successful'
        return response

