import re

def is_phishing_email(email_subject, email_body):
    """
    Detect TikTok-specific phishing emails using regex-based pattern matching on both subject and body.
    """
    # TikTok-related phishing patterns
    tiktok_phishing_patterns = [
    # Suspicious URLs or phishing links within the body or subject
    r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
    r'https?://(?!www\.tiktok\.com)[a-zA-Z0-9-]+\.tiktok\.com',  # Fake TikTok domains

    # Credential theft or phishing attempts related to TikTok in the subject or body
    r'(?:tiktok|your tiktok account|tiktok support).*?(?:reset|verify|update|confirm|login|recover)',

    r'(?:your tiktok account is|has been) (?:suspended|compromised|locked|disabled)',
    # Urgent actions related to TikTok accounts
    r'\b(?:urgent action required for your tiktok account)\b',
    r'\b(?:verify your tiktok account)\b',
    r'\b(?:click here to secure your tiktok account)\b',

    # Suspicious email domains pretending to be from TikTok
    r'from:\s*[a-zA-Z0-9._%+-]+@(?!tiktok\.com)[a-zA-Z0-9.-]+(?:\.com|\.net|\.org)',  # Adjusted to common domains

    # Additional patterns to detect phishing attempts
    r'download|install|update|activate',  # Suspicious actions
    r'account|password|credentials',  # Sensitive information
    r'warning|alert|notification',  # Urgent language

    # TikTok-specific phishing patterns
 r'tiktok login|tiktok sign in',  # Fake TikTok login pages
    r'tiktok account verification',  # Fake TikTok account verification
    r'tiktok password reset',  # Fake TikTok password reset
    r'tiktok security alert',  # Fake TikTok security alerts
    r'tiktok account suspended',  # Fake TikTok account suspension
    r'tiktok account compromised',  # Fake TikTok account compromise
]

    # Compile the regex pattern for TikTok phishing
    tiktok_phishing_regex = re.compile('|'.join(tiktok_phishing_patterns), re.IGNORECASE)

    # Check both the subject and body for TikTok phishing patterns
    if tiktok_phishing_regex.search(email_subject) or tiktok_phishing_regex.search(email_body):
        return True

    return False
