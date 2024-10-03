from django.urls import path

from .views import OAuthAuthorizeView, OAuthRedirectView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('oauth-redirect/', OAuthRedirectView.as_view(), name='connect_email'),
    path('oauth-authorize/', OAuthAuthorizeView.as_view(), name='oauth-authorize'), #new
]
