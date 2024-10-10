from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from .models import SpamEmail, CustomUser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from dj_rest_auth.serializers import LoginSerializer

User = get_user_model()


# Serializer for SpamEmail model
class SpamEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamEmail
        fields = ['id', 'message_id', 'sender', 'subject', 'body', 'detected_on']


# Custom serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def create(self, validated_data):
        if validated_data['password1'] != validated_data['password2']:
            raise serializers.ValidationError("Passwords do not match.")

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password1'])  # Hash the password
        user.save()
        return user


# Custom serializer for user login
class CustomLoginSerializer(LoginSerializer):
    username = None  # Remove the username field
    email = serializers.EmailField(required=True, allow_blank=False)  # Use email instead

    def get_auth_user(self, email, password):
        # Override the default method to use email for authentication
        user = self.context['request'].user
        if user and user.is_authenticated:
            return user

        try:
            # Perform authentication using email instead of username
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(_("Invalid email/password."))

        if user and user.check_password(password):
            return user

        raise serializers.ValidationError(_("Invalid email/password."))

