import os

from config.logging import logger


def log_and_print(message, level="info"):
    getattr(logger, level)(message)
    print(message)


def log_email_summary(total_sent, len_recipients, dry_run=False):
    if dry_run:
        log_and_print(
            f"Dry run succeeded. No emails were sent.")
    if not dry_run:
        log_and_print(f"Successfully sent {
                      total_sent}/{len_recipients} emails.")


def log_success(index, recipient, recipients, sent_attachments, success, attachments):
    failed_recipients, successful_attachments, = [], set()

    if success:
        log_and_print(f"{index}/{len(recipients)} Successfully sent email to {
                      recipient['email']}")
        if attachments:
            successful_attachments.update(str(a) for a in sent_attachments)
            logger.info(f"{index}/{len(recipients)} Attachments sent to {recipient['email']}: {
                [os.path.basename(a) for a in sent_attachments]}")
        else:
            logger.info(f"No attachments included.")
    else:
        failed_recipients.append(recipient['email'])
        log_and_print(f"{index}/{len(recipients)} Failed to send email to {
                      recipient['email']}", "error")
