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

# First check if the email is TikTok-related
tiktok_related_patterns = [
    r'\btiktok\b',
    r'(?:^|\s)tt\b',  # Common TikTok abbreviation
    r'douyin',  # TikTok's Chinese name
    r'musical\.ly',  # TikTok's previous name
]

# Compile TikTok-related pattern
tiktok_related_regex = re.compile('|'.join(tiktok_related_patterns), re.IGNORECASE)

# More specific phishing patterns that only apply to TikTok-related content
tiktok_phishing_patterns = [
    # Fake TikTok domains - more specific
    r'https?://(?!(?:www\.)?tiktok\.com)[a-zA-Z0-9-]+[^/]*(?:tiktok|tiktak|tiktoc|tiktk)[^/]*\.(?:com|net|org|info|online)',
    
    # TikTok-specific suspicious verification links
    r'https?://[^/]+/(?:tiktok|tt)-?(?:verify|login|account)',
    
    # Credential theft specifically mentioning TikTok
    r'tiktok.*?(?:verify|confirm).*?(?:account|identity|login)',
    r'(?:your tiktok account|tiktok profile).*?(?:suspended|compromised|locked|disabled)',
    
    # Urgent TikTok-specific actions
    r'urgent.*?tiktok.*?(?:verify|confirm|login)',
    r'(?:verify|confirm).*?tiktok.*?(?:now|immediately|urgent)',
    
    # TikTok-specific credential harvesting
    r'tiktok.*?(?:password|login|credentials).*?(?:update|reset|confirm)',
    
    # Suspicious TikTok reward/verification promises
    r'tiktok.*?(?:verified badge|verification|blue tick).*?(?:click|visit|apply)',
    r'tiktok.*?(?:followers|likes|views).*?(?:free|boost|increase)',
]

# Compile TikTok phishing patterns
tiktok_phishing_regex = re.compile('|'.join(tiktok_phishing_patterns), re.IGNORECASE)

def is_phishing_email(email_subject, email_body, email_sender):
    """
    Detect TikTok-specific phishing emails using a two-step verification process:
    1. First checks if the email is TikTok-related
    2. If TikTok-related, then checks for phishing patterns
    
    Parameters:
        email_subject (str): The subject line of the email
        email_body (str): The body content of the email
        email_sender (str): The email address of the sender
        
    Returns:
        bool: True if the email is suspected to be TikTok-related phishing, False otherwise
    """
    # Normalize inputs
    email_sender = email_sender.lower()
    combined_content = f"{email_subject} {email_body}".lower()
    
    # Check whitelist first
    if email_sender in tiktok_whitelist:
        return False
        
    # Step 1: Check if the email is TikTok-related
    is_tiktok_related = bool(tiktok_related_regex.search(combined_content))
    
    # If not TikTok-related, return False immediately
    if not is_tiktok_related:
        return False
        
    # Step 2: Only check for phishing patterns if the email is TikTok-related
    return bool(tiktok_phishing_regex.search(combined_content))
