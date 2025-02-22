import mimetypes
import os
import re
import sys

from config.logging import logger
from config.settings import (ATTACHMENT_ALLOWED_MIME_TYPES, ATTACHMENT_IGNORED_EXTENSIONS,
                             ATTACHMENT_MAX_SIZE, PATTERN_EMAIL, PATTERN_NAME)
from scripts.utils import log_and_print


def validate_recipients(recipients):
    if not recipients:
        logger.error("No valid recipients found")
        raise ValueError("No valid recipients found")

    email_to_names = {}

    for recipient in recipients:
        if not validate_pattern(recipient['name'], PATTERN_NAME):
            raise ValueError(f"Invalid name: {recipient['name']}")
        if not validate_pattern(recipient['email'], PATTERN_EMAIL):
            raise ValueError(f"Invalid name: {recipient['name']}")
        if not check_email_name_conflicts(recipient, email_to_names):
            raise ValueError(f"Found email duplicates under different names: {recipient['email']} - {
                             email_to_names[recipient['email']]}\nPlease remove duplicates from the CSV file.")
    return recipients


def check_email_name_conflicts(recipient, email_to_names):
    email = recipient['email']

    if email in email_to_names:
        if recipient['name'] not in email_to_names[email]:
            email_to_names[email].append(recipient['name'])
            return False
    else:
        email_to_names[email] = [recipient['name']]

    return True


def validate_pattern(value, pattern):
    return bool(re.match(pattern, value))


def validate_attachments(attachments):
    if not attachments:
        return [], []

    valid_attachments = []

    for attachment in attachments:
        if not os.path.exists(attachment):
            log_and_print(f"Attachment not found: {attachment}", "error")
            continue

        attachment_name = os.path.basename(attachment)

        if any(attachment_name.endswith(ext) for ext in ATTACHMENT_IGNORED_EXTENSIONS):
            file_ext = os.path.splitext(attachment_name)[1] if os.path.splitext(
                attachment_name)[1] else os.path.splitext(attachment_name)[0]
            logger.info(f"{attachment} is ignored: File extension '{
                        file_ext}' is on ignore list")
            continue

        file_size = os.path.getsize(attachment)
        if file_size > ATTACHMENT_MAX_SIZE:
            log_and_print(f"File '{attachment_name}' cannot be attached: Exceeding size limit ({
                file_size/1024/1024:.1f}MB > {ATTACHMENT_MAX_SIZE/1024/1024:.1f}MB)", "warning")
            abort = True
            break

        content_type, encoding = mimetypes.guess_type(attachment)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        if not any(content_type == allowed or (allowed.endswith('/*') and content_type.startswith(allowed[:-2])) for allowed in ATTACHMENT_ALLOWED_MIME_TYPES):
            log_and_print(f"File '{
                attachment_name}' cannot be attached: Unsupported MIME type ({content_type}).", "warning")
            abort = True
            break

        valid_attachments.append(attachment)

    try:
        if abort:
            sys.exit(
                "\nPlease delete the file from the attachments folder or update config/settings.py accordingly.")
    except NameError:
        pass

    return valid_attachments
