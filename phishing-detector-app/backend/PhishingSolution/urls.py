from django.urls import path
from .views import SpamDetectionAPIView

urlpatterns = [
    path('start-detection/', SpamDetectionAPIView.as_view(), name='start-detection'),
]
