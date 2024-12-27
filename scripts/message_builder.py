from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import os
from markdown import markdown
from config.settings import ALLOWED_MIME_TYPES, MAX_ATTACHMENT_SIZE

def create_base_message(to_email, subject):
    message = MIMEMultipart('mixed')
    message['to'] = to_email
    message['subject'] = subject
    return message

def create_content_parts(content):
    html_content = markdown(content, extensions=['extra'])
    text_part = MIMEText(content, 'plain')
    html_part = MIMEText(html_content, 'html')
    return text_part, html_part

def add_attachments(message, attachments):
    if not attachments:
        return [], []

    successful_attachments = []
    skipped_attachments = []

    for filepath in attachments:
        if not os.path.exists(filepath):
            skipped_attachments.append((filepath, "Attachment not found"))
            continue

        # Check file size
        file_size = os.path.getsize(filepath)
        if file_size > MAX_ATTACHMENT_SIZE:
            skipped_attachments.append((filepath, f"Exceeds size limit ({file_size/1024/1024:.1f}MB > {MAX_ATTACHMENT_SIZE/1024/1024:.1f}MB)"))
            continue

        content_type, encoding = mimetypes.guess_type(filepath)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        # Check if MIME type is allowed
        if not any(content_type == allowed or (allowed.endswith('/*') and content_type.startswith(allowed[:-2])) for allowed in ALLOWED_MIME_TYPES):
            skipped_attachments.append((filepath, f"Unsupported MIME type ({content_type})"))
            continue

        main_type, sub_type = content_type.split('/', 1)

        with open(filepath, 'rb') as attachment:
            part = MIMEBase(main_type, sub_type)
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            filename = os.path.basename(filepath)
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(part)
            successful_attachments.append(filepath)

    return successful_attachments, skipped_attachments