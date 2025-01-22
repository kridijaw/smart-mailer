from datetime import time

EMAIL_PREVIEW_ENABLED = True  # Set to False to disable email preview in terminal
EMAIL_MAX_RETRY_ATTEMPTS = 5  # Number of retry attempts for sending an email

# Attachment settings
ATTACHMENT_MAX_SIZE = 60 * 1024 * 1024  # per file in bytes (default: 60MB)
ATTACHMENT_IGNORED_EXTENSIONS = ['.DS_Store']  # Ignored file extensions
ATTACHMENT_ALLOWED_MIME_TYPES = ['application/pdf',
                                 'image/*', 'video/*', 'audio/*', 'text/*']  # Allowed MIME types

# Allowed patterns for email and name
PATTERN_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-ZğüşöçİĞÜŞÖÇ]{2,}$'
PATTERN_NAME = r'^[a-zA-ZğüşöçİĞÜŞÖÇ\s]{2,}$'
