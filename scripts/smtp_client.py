from base64 import urlsafe_b64encode
from googleapiclient.discovery import build
from scripts.get_credentials import get_credentials
from email.mime.multipart import MIMEMultipart
from scripts.message_builder import create_base_message, create_content_parts, add_attachments
from config.settings import MAX_RETRY_ATTEMPTS
import time

def send_email(to_email, subject, content, attachments=None):
    """Sends an HTML email with optional attachments using the Gmail API."""
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # Build the message
    message = create_base_message(to_email, subject)
    msg_alternative = MIMEMultipart('alternative')
    message.attach(msg_alternative)

    # Add content
    text_part, html_part = create_content_parts(content)
    msg_alternative.attach(text_part)
    msg_alternative.attach(html_part)

    # Add attachments
    add_attachments(message, attachments)

    # Send the email with retries
    raw_message = urlsafe_b64encode(message.as_bytes()).decode()
    
    for attempt in range(MAX_RETRY_ATTEMPTS):
        try:
            service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
            return True
        except Exception as e:
            if attempt < MAX_RETRY_ATTEMPTS - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff
                print(f"\nRetry {attempt + 1}/{MAX_RETRY_ATTEMPTS} for {to_email} after {wait_time}s: {e}")
                time.sleep(wait_time)
            else:
                print(f"\nFailed to send email to {to_email} after {MAX_RETRY_ATTEMPTS} attempts: {e}")
                return False