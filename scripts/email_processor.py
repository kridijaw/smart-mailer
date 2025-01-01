import os

from config.logging import logger
from scripts.email_summary import summarize_email_info
from scripts.smtp_client import send_email
from scripts.template_manager import render_template
from scripts.utils import log_and_print


def process_recipients(recipients, attachments, template_path):
    total_sent, failed_recipients, successful_attachments, skipped_attachments = 0, [], set(), set()

    for index, recipient in enumerate(recipients, start=1):

        log_and_print(f"{index}/{len(recipients)} Processing email for {
            recipient['name']} ({recipient['email']})")

        subject, email_content = render_template(template_path, recipient)

        success, attach_result = send_email(
            recipient["email"], subject, email_content, index, recipients, attachments)

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
