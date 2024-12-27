import logging
from datetime import datetime
import os

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Configure logging
logger = logging.getLogger('smart_mailer')
logger.setLevel(logging.INFO)

# Create handlers
file_handler = logging.FileHandler(f'logs/smart_mailer.log')
console_handler = logging.StreamHandler()

# Create formatters and add it to handlers
log_format = '%(asctime)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)