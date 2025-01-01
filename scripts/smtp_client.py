import io
import time
from email.mime.multipart import MIMEMultipart

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from tqdm import tqdm

from config.settings import MAX_RETRY_ATTEMPTS
from scripts.get_credentials import get_credentials
from scripts.message_builder import (add_attachments, create_base_message,
                                     create_content_parts)


def send_email(to_email, subject, content, index, recipients, attachments=None):
    """Sends an HTML email with a resumable (chunked) upload for large attachments,
    allowing a progress bar to track upload progress.
    """
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
    successful_attachments = add_attachments(message, attachments)

    # Prepare the message data for a resumable upload
    raw_bytes = message.as_bytes()
    fd = io.BytesIO(raw_bytes)
    media = MediaIoBaseUpload(
        fd, mimetype='message/rfc822', chunksize=256*1024, resumable=True)

    # Build the send request (body can remain empty since 'raw' is uploaded via media_body)
    request = service.users().messages().send(
        userId='me', media_body=media, body={})

    # Show a progress bar for the entire size of the message (including attachments)
    total_size = len(raw_bytes)
    pbar = tqdm(total=total_size, unit='B', unit_scale=True,
                desc=f"{index}/{len(recipients)} Sending to {to_email}", mininterval=0.1,
                smoothing=0.1
                )

    response = None
    attempt = 0

    # Retry loop (if desired)
    while attempt < MAX_RETRY_ATTEMPTS and response is None:
        try:
            status, response = request.next_chunk()
            if status:
                # Update the progress bar by how many bytes have been uploaded so far
                pbar.update(status.resumable_progress - pbar.n)
        except Exception as e:
            attempt += 1
            if attempt < MAX_RETRY_ATTEMPTS:
                wait_time = (attempt) * 2  # Simple exponential backoff
                print(f"\nRetry {attempt}/{MAX_RETRY_ATTEMPTS} for {to_email} "
                      f"after {wait_time}s due to error: {e}")
                time.sleep(wait_time)
                continue
            else:
                print(f"\nFailed to send email to {to_email} after {
                      MAX_RETRY_ATTEMPTS} attempts: {e}")
                pbar.close()
                return False, (successful_attachments)

    # Final update to ensure the bar reaches 100%
    if pbar.n < total_size:
        pbar.update(total_size - pbar.n)

    pbar.close()

    # If the upload is successful, response should contain the message resource ID
    if response is not None and 'id' in response:
        return True, (successful_attachments)
    else:
        return False, (successful_attachments)
