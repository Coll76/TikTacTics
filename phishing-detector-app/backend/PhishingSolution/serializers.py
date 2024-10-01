from rest_framework import serializers
from .models import User, PhishingLink, PhishingData

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active')  # Add any additional fields you want to expose

class PhishingLinkSerializer(serializers.ModelSerializer):
    """Serializer for the PhishingLink model."""
    
    class Meta:
        model = PhishingLink
        fields = ('id', 'url', 'created_at')

class PhishingDataSerializer(serializers.ModelSerializer):
    """Serializer for the PhishingData model."""
    
    class Meta:
        model = PhishingData
        fields = ('id', 'link', 'phishing', 'created_at')
