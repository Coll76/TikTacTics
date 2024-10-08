from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import is_phishing_email  # Import the TikTok phishing detection logic

class SpamDetectionAPIView(APIView):
    def post(self, request):
        emails = request.data.get('emails', [])

        if not emails:
            return Response({"error": "No emails provided"}, status=status.HTTP_400_BAD_REQUEST)

        detected_spam_emails = []

        # Iterate through each email and detect if it's phishing (TikTok specific)
        for email in emails:
            # Extract important fields from each email
            message_id = email.get('messageID', '')
            sender = email.get('from', '')
            subject = email.get('subject', '')
            body = email.get('body', '')

            # Use the TikTok phishing detection logic
            if is_phishing_email(subject, body):
                # Add the detected phishing email's data to the list
                detected_spam_emails.append({
                    'messageID': message_id,
                    'from': sender,
                    'subject': subject,
                    'body': body
                })

        # Return the list of detected phishing emails to the mobile app
        return Response({
            "spam_emails": detected_spam_emails
        }, status=status.HTTP_200_OK)
