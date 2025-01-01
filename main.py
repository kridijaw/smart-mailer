import mimetypes
import os
import sys

from config.logging import logger
from config.settings import (ALLOWED_MIME_TYPES, IGNORED_EXTENSIONS,
                             MAX_ATTACHMENT_SIZE, MAX_RETRY_ATTEMPTS,
                             PREVIEW_EMAIL)
from scripts.cli import parse_arguments
from scripts.csv_manager import load_recipients
from scripts.preview_emails import preview_emails
from scripts.smtp_client import send_email
from scripts.template_manager import render_template


def load_data():
    recipients = load_recipients("data/recipients.csv")
    attachments_folder = "attachments"
    attachments = [
        os.path.join(attachments_folder, f)
        for f in os.listdir(attachments_folder)
        if os.path.isfile(os.path.join(attachments_folder, f))
    ]
    return recipients, attachments


def log_and_print(message, level="info"):
    getattr(logger, level)(message)
    print(message)


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


def process_recipients(recipients, attachments, template_path):
    total_sent, failed_recipients, successful_attachments, skipped_attachments = 0, [], set(), set()

    for index, recipient in enumerate(recipients, start=1):

        log_and_print(f"{index}/{len(recipients)} Processing email for {
            recipient['name']} ({recipient['email']})")

        subject, email_content = render_template(template_path, recipient)

        success, attach_result = send_email(
            recipient["email"], subject, email_content, attachments)

        if success:
            total_sent += 1
            sent_attachments, skipped_attachments, ignored_attachments = attach_result
            successful_attachments.update(str(a) for a in sent_attachments)
            log_and_print(f"{index}/{len(recipients)} Successfully sent email to {
                          recipient['email']}")
            logger.info(f"{index}/{len(recipients)} Attachments sent to {recipient['email']}: {
                [os.path.basename(a) for a in sent_attachments]}")
        else:
            failed_recipients.append(recipient['email'])
            log_and_print(f"{index}/{len(recipients)} Failed to send email to {
                          recipient['email']}", "error")

        if skipped_attachments:
            log_and_print(f"{index}/{len(recipients)} Skipped attachments for {recipient['email']}: {
                [os.path.basename(a) for a, _ in skipped_attachments]}", "warning")

        if ignored_attachments:
            logger.info(f"{index}/{len(recipients)} Ignored attachments for {recipient['email']}: {
                [os.path.basename(a) for a, _ in ignored_attachments]}")

    summarize_email_info(total_sent, recipients, failed_recipients,
                         successful_attachments, skipped_attachments)
    return total_sent, failed_recipients, successful_attachments, skipped_attachments


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


def main():
    try:
        args = parse_arguments()
        dry_run = args.dry_run
        if not (dry_run):
            logger.info('Starting Smart Mailer application')
        template_path = "data/email_template.txt"

        recipients, attachments = load_data()
        check_attachments(attachments)

        if not recipients:
            logger.error("No valid recipients found")
            raise ValueError("No valid recipients found")

        if dry_run or PREVIEW_EMAIL:
            preview_emails(recipients[0], template_path, attachments)

        if not dry_run:
            process_recipients(
                recipients, attachments, template_path)

    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}", exc_info=True)
        print(f"\nError in main: {e}")
        raise


if __name__ == "__main__":
    main()
