from datetime import time

EMAIL_PREVIEW_ENABLED = True
MAX_RETRY_ATTEMPTS = 5

MAX_ATTACHMENT_SIZE = 60 * 1024 * 1024  # 60MB
ALLOWED_MIME_TYPES = ['application/pdf',
                      'image/*', 'video/*', 'audio/*', 'text/*']
IGNORED_EXTENSIONS = ['.DS_Store']

SCHEDULING_ENABLED = True
SEND_TIME_START = time(0, 0)  # 24-hour HH:MM format
SEND_TIME_END = time(23, 59)
