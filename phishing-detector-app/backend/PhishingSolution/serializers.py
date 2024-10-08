# serializers.py

from rest_framework import serializers
from .models import SpamEmail

class SpamEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamEmail
        fields = ['id', 'message_id', 'sender', 'subject', 'body', 'detected_on']
        read_only_fields = ['id', 'detected_on']  # detected_on is read-only since it's auto-added
