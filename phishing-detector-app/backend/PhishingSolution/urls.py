from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SpamDetectionAPIView, PhishingRegisterView, CustomLoginView, CustomLogoutView, PasswordResetRequestView, PasswordResetView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('start-detection/', SpamDetectionAPIView.as_view(), name='start-detection'),
    path('auth/register/', PhishingRegisterView.as_view(), name='auth_register'),
    path('auth/login/', CustomLoginView.as_view(), name='auth_login'),
    path('auth/logout/', CustomLogoutView.as_view(), name='auth_logout'),
    
    # Include the dj_rest_auth URLs
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/', include('dj_rest_auth.registration.urls')),

    #new
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('reset/<uidb64>/<token>/', PasswordResetView.as_view(), name='password-reset-confirm'),
]

