import mimetypes
import os
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from markdown import markdown

from config.settings import (ATTACHMENT_ALLOWED_MIME_TYPES, ATTACHMENT_IGNORED_EXTENSIONS,
                             ATTACHMENT_MAX_SIZE)


def create_base_message(to_email, subject, reply_to=None):
    message = MIMEMultipart('mixed')
    message['to'] = to_email
    message['subject'] = subject
    if reply_to:
        message['reply-to'] = reply_to
    return message


def create_content_parts(content):
    html_content = markdown(content, extensions=['extra'])
    text_part = MIMEText(content, 'plain')
    html_part = MIMEText(html_content, 'html')
    return text_part, html_part


def add_attachments(message, attachments):
    if not attachments:
        return [], []

    sorted_attachments = sorted(attachments, key=natural_sort_key)
    successful_attachments = []

    for filepath in sorted_attachments:
        if not os.path.exists(filepath):
            continue

        attachment_name = os.path.basename(filepath)

        if any(attachment_name.endswith(ext) for ext in ATTACHMENT_IGNORED_EXTENSIONS):
            continue

        file_size = os.path.getsize(filepath)
        if file_size > ATTACHMENT_MAX_SIZE:
            continue

        content_type, encoding = mimetypes.guess_type(filepath)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        if not any(
            content_type == allowed or (allowed.endswith(
                '/*') and content_type.startswith(allowed[:-2]))
            for allowed in ATTACHMENT_ALLOWED_MIME_TYPES
        ):
            continue

        main_type, sub_type = content_type.split('/', 1)

        with open(filepath, 'rb') as attachment:
            part = MIMEBase(main_type, sub_type)
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            filename = os.path.basename(filepath)
            part.add_header('Content-Disposition',
                            'attachment', filename=filename)
            message.attach(part)
            successful_attachments.append(filepath)

    return successful_attachments


def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split('([0-9]+)', s)]
