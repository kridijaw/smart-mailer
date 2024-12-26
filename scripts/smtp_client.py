from googleapiclient.discovery import build
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from config import get_credentials

def send_email(to_email, subject, content):
    """Sends an email using the Gmail API."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEText(content)
    message['to'] = to_email
    message['subject'] = subject
    raw_message = urlsafe_b64encode(message.as_bytes()).decode()

    try:
        message = service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
        print(f"Email sent to {to_email} ✔")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")