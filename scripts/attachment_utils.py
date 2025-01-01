import mimetypes
import os
import sys

from config.settings import (ALLOWED_MIME_TYPES, IGNORED_EXTENSIONS,
                             MAX_ATTACHMENT_SIZE)


def check_attachments(attachments):
    if not attachments:
        return [], []

    skipped_attachments = []

    for attachment in attachments:
        if not os.path.exists(attachment):
            skipped_attachments.append((attachment, "Attachment not found"))
            continue

        attachment_name = os.path.basename(attachment)

        if any(attachment_name.endswith(ext) for ext in IGNORED_EXTENSIONS):
            skipped_attachments.append((attachment, f"File extension '{
                                       os.path.splitext(attachment_name)[1]}' is ignored"))
            continue

        file_size = os.path.getsize(attachment)
        if file_size > MAX_ATTACHMENT_SIZE:
            print(f"File '{attachment_name}' cannot be attached: Exceeding size limit ({
                  file_size/1024/1024:.1f}MB > {MAX_ATTACHMENT_SIZE/1024/1024:.1f}MB)")
            abort = True
            break

        content_type, encoding = mimetypes.guess_type(attachment)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        if not any(content_type == allowed or (allowed.endswith('/*') and content_type.startswith(allowed[:-2])) for allowed in ALLOWED_MIME_TYPES):
            print(f"File '{
                  attachment_name}' cannot be attached: Unsupported MIME type ({content_type}).")
            abort = True
            break

    try:
        if abort:
            print(
                "\nPlease delete the file from the attachments folder or update config/settings.py accordingly.")
            sys.exit("Stopping the application.")
    except NameError:
        pass
