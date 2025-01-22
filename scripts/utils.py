import os

from config.logging import logger
from scripts.csv_manager import load_recipients


def log_and_print(message, level="info"):
    getattr(logger, level)(message)
    print(message)


def load_data():
    recipients = load_recipients("data/recipients.csv")
    attachments_folder = "attachments"
    attachments = [
        os.path.join(attachments_folder, f)
        for f in os.listdir(attachments_folder)
        if os.path.isfile(os.path.join(attachments_folder, f))
    ]
    return recipients, attachments


def log_email_summary(total_sent, len_recipients):
    log_and_print(f"Successfully sent {total_sent}/{len_recipients} emails")


def log_success(index, recipient, len_recipients, sent_attachments, success, attachments):
    failed_recipients, successful_attachments, = [], set()

    if success:
        log_and_print(f"{index}/{len_recipients} Successfully sent email to {
                      recipient['email']}")
        if attachments:
            successful_attachments.update(str(a) for a in sent_attachments)
            logger.info(f"{index}/{len_recipients} Attachments sent to {recipient['email']}: {
                [os.path.basename(a) for a in sent_attachments]}")
        else:
            logger.info(f"No attachments included.")
    else:
        failed_recipients.append(recipient['email'])
        log_and_print(f"{index}/{len_recipients} Failed to send email to {
                      recipient['email']}", "error")
