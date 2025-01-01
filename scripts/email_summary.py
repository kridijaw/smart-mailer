import os

from config.logging import logger
from config.settings import MAX_RETRY_ATTEMPTS
from scripts.utils import log_and_print


def summarize_email_info(total_sent, recipients, failed_recipients,
                         successful_attachments, skipped_attachments):
    log_and_print(f"\nSummary: Successfully sent {
        total_sent}/{len(recipients)} emails")
    if failed_recipients:
        log_and_print(f"Failed recipients: {failed_recipients} after {
                      MAX_RETRY_ATTEMPTS}", "error")
    if successful_attachments:
        log_and_print(f"Sent attachments: {
            [os.path.basename(a) for a in successful_attachments]}")
    if skipped_attachments:
        logger.warning(f"Skipped attachments: {
            [(os.path.basename(a), r) for a, r in skipped_attachments]}")
        print("\nAttachments that were not sent and reasons:")
        for attachment, reason in skipped_attachments:
            print(f"- {os.path.basename(attachment)}: {reason}")
        print(
            "\nPlease check the attachments folder or update the config/settings.py accordingly.")
