from rest_framework import serializers
from .models import EmailMessage

class OAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=255)
    token_type = serializers.CharField(max_length=255)
    expires_in = serializers.IntegerField()
    refresh_token = serializers.CharField(max_length=255)

class EmailMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailMessage
        fields = ['id', 'subject', 'body', 'sender', 'recipient', 'created_at']

class OAuthAuthorizeSerializer(serializers.Serializer):
    auth_url = serializers.URLField()

class OAuthRedirectSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=255)
