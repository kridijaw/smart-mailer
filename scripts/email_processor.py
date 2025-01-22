from scripts.scheduler import wait_for_send_window
from scripts.smtp_client import send_email
from scripts.template_manager import render_template
from scripts.utils import log_email_summary, log_success


def process_email(recipients, template_path, attachments, dry_run):
    if not dry_run:
        total_sent = 0

        for index, recipient in enumerate(recipients, start=1):
            wait_for_send_window()

            email_subject, email_content, reply_to = render_template(
                template_path, recipient)

            success, sent_attachments = send_email(
                index, recipient, email_subject, email_content, attachments, reply_to)

            if success:
                total_sent += 1

            log_success(index, recipient, len(
                recipients), sent_attachments, success, attachments)

        log_email_summary(total_sent, len(recipients), dry_run)
