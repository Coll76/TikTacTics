# myapp/utils.py
import imaplib

def fetch_email_messages(access_token):
    # Connect to the IMAP server
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.authenticate('XOAUTH2', access_token)

    # Select the inbox
    imap.select('inbox')

    # Search for email messages
    status, messages = imap.search(None, 'ALL')

    # Fetch the email messages
    for num in messages[0].split():
        status, msg = imap.fetch(num, '(RFC822)')
        raw_message = msg[0][1]

        # Parse the email message
        # ...

    imap.logout()
