import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

# Whitelist of legitimate TikTok email addresses and domains (case-insensitive)
tiktok_whitelist = {
    'support@tiktok.com',
    'info@tiktok.com',
    'notifications@tiktok.com',
    'alerts@tiktok.com',
    'security@tiktok.com',
    'tiktok.com',
    'www.tiktok.com'
}

# Compile the regex pattern for TikTok phishing
tiktok_phishing_patterns = [
    # Fake TikTok domains
    r'https?://(?!www\.tiktok\.com)[a-zA-Z0-9-]+\.tiktok\.com',
    
    # Suspicious verification links
    r'https?://[a-zA-Z0-9-]+\.(com|net|org)/verify',
    
    # Credential theft or phishing attempts related to TikTok
    r'(?:tiktok|your tiktok account|tiktok support).*(?:reset|verify|update|confirm|login|recover).*(?:password|credentials)',
    
    r'(?:your tiktok account is|has been) (?:suspended|compromised|locked|disabled).*(?:click|visit|login)',
    
    # Urgent actions related to TikTok accounts
    r'\b(?:urgent action required for your tiktok account)\b',
    r'\b(?:verify your tiktok account)\b',
    r'\b(?:click here to secure your tiktok account)\b',
    
    # Suspicious email domains pretending to be from TikTok
    r'from:\s*[a-zA-Z0-9._%+-]+@(?!tiktok\.com)[a-zA-Z0-9.-]+(?:\.com|\.net|\.org)',
    
    # Additional patterns to detect phishing attempts
    r'download|install|update|activate.*?(?:password|credentials)',  # Suspicious actions
    r'warning|alert|notification.*?(?:password|credentials)',  # Urgent language
    
    # TikTok-specific phishing patterns
    r'tiktok login|tiktok sign in.*?(?:password|credentials)',  # Fake TikTok login pages
    r'tiktok account verification.*?(?:password|credentials)',  # Fake TikTok account verification
    r'tiktok password reset.*?(?:password|credentials)',  # Fake TikTok password reset
    r'tiktok security alert.*?(?:password|credentials)',  # Fake TikTok security alerts
    r'tiktok account suspended.*?(?:password|credentials)',  # Fake TikTok account suspension
    r'tiktok account compromised.*?(?:password|credentials)',  # Fake TikTok account compromise
]

# Compile all patterns into a single regex for efficiency
tiktok_phishing_regex = re.compile('|'.join(tiktok_phishing_patterns), re.IGNORECASE)

def is_phishing_email(email_subject, email_body, email_sender):
    """
    Detect TikTok-specific phishing emails using regex-based pattern matching on both the subject and body.

    Parameters:
        email_subject (str): The subject line of the email.
        email_body (str): The body content of the email.
        email_sender (str): The email address of the sender.

    Returns:
        bool: True if the email is suspected to be phishing, False otherwise.
    """
    # Normalize the email sender to lowercase for case-insensitive comparison
    email_sender = email_sender.lower()

    # Check if the email sender is in the whitelist
    if email_sender in tiktok_whitelist:
        return False

    # Check both the subject and body for TikTok phishing patterns
    if tiktok_phishing_regex.search(email_subject) or tiktok_phishing_regex.search(email_body):
        return True

    return False
