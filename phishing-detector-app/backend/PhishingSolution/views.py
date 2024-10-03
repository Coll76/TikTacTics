from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import OAuthSerializer, OAuthAuthorizeSerializer, EmailMessageSerializer
import requests
from urllib.parse import urlencode

class OAuthRedirectView(APIView):
    def get(self, request):
        # Get the authorization code from the request
        code = request.GET.get('code')

        # Check if the code is None
        if not code:
            return Response({"error": "Authorization code is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Exchange the authorization code for an access token
        token_url = 'https://oauth2.googleapis.com/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://127.0.0.1:8000/api/v1/oauth-redirect/',
            'client_id': '344719165870-kb3l6s01e3s7c3v4rfllpamffa05jf8p.apps.googleusercontent.com',
            'client_secret': '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',
        }

        # Handle errors when making requests to Google's OAuth API
        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code != 200:
            return Response(response.json(), status=response.status_code)

        # Get the access token from the response
        access_token = response.json().get('access_token')
        token_type = response.json().get('token_type')
        expires_in = response.json().get('expires_in')
        refresh_token = response.json().get('refresh_token')

        # Serialize the access token response
        serializer = OAuthSerializer(data={
            'access_token': access_token,
            'token_type': token_type,
            'expires_in': expires_in,
            'refresh_token': refresh_token,
        })
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OAuthAuthorizeView(APIView):
    def get(self, request):
        # Initiate the OAuth flow
        auth_url = 'https://accounts.google.com/o/oauth2/auth'
        params = {
            'response_type': 'code',
            'client_id': '344719165870-kb3l6s01e3s7c3v4rfllpamffa05jf8p.apps.googleusercontent.com',
            'redirect_uri': 'http://127.0.0.1:8000/api/v1/oauth-redirect/',
            'scope': 'https://www.googleapis.com/auth/gmail.readonly',
        }
        # Build the authorization URL manually
        full_auth_url = f"{auth_url}?{urlencode(params)}"

        # Serialize the authorization URL
        serializer = OAuthAuthorizeSerializer(data={'auth_url': full_auth_url})
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmailMessageView(APIView):

    def get(self, request):
        # Fetch the email messages
        email_messages = EmailMessage.objects.all()
        # Serialize the email message data
        serializer = EmailMessageSerializer(email_messages, many=True)
        # Call the phishing detection function
        phishing_detection_results = self.phishing_detection(serializer.data)
        return Response(phishing_detection_results, status=status.HTTP_200_OK)

    def phishing_detection(self, email_messages):
        # Implement phishing Detection Logic Here
        pass
