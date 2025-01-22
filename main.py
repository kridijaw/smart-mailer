from config.logging import logger
from config.settings import EMAIL_PREVIEW_ENABLED
from scripts.attachment_utils import validate_attachments
from scripts.cli import parse_arguments
from scripts.preview_emails import preview_emails
from scripts.scheduler import wait_for_send_window
from scripts.smtp_client import send_email
from scripts.template_manager import render_template
from scripts.utils import load_data, log_email_summary, log_success


def main():
    try:
        args = parse_arguments()
        dry_run = args.dry_run
        if not (dry_run):
            logger.info('Starting Smart Mailer application')
        template_path = "data/email_template.txt"

        recipients, attachments = load_data()
        attachments = validate_attachments(attachments)

        if not recipients:
            logger.error("No valid recipients found")
            raise ValueError("No valid recipients found")

        if dry_run or EMAIL_PREVIEW_ENABLED:
            preview_emails(recipients[0], template_path, attachments)

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

            log_email_summary(total_sent, len(recipients))

    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}", exc_info=True)
        print(f"\nError in main: {e}")
        raise


if __name__ == "__main__":
    main()
