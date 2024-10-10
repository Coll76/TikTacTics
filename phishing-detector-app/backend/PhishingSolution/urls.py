from django.urls import path, include
from .views import SpamDetectionAPIView, PhishingRegisterView, CustomLoginView, CustomLogoutView
from .consumers import SpamEmailConsumer  # Import your WebSocket consumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from allauth.account.views import confirm_email


# Define the WebSocket URL patterns here
websocket_urlpatterns = [
    path('ws/spam-alerts/', SpamEmailConsumer.as_asgi()),  # WebSocket URL for spam alerts
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})

urlpatterns = [
    path('start-detection/', SpamDetectionAPIView.as_view(), name='start-detection'),
    path('auth/register/', PhishingRegisterView.as_view(), name='auth_register'),
    path('auth/login/', CustomLoginView.as_view(), name='auth_login'),
    path('auth/logout/', CustomLogoutView.as_view(), name='auth_logout'),
    # Email confirmation URL
    #path('auth/account-confirm-email/<str:key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
    #path('verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify_email'),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/', include('dj_rest_auth.registration.urls')),
]
