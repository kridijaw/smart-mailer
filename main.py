from config.logging import logger
from config.settings import EMAIL_PREVIEW_ENABLED
from scripts.cli import parse_arguments
from scripts.data_loader import load_data
from scripts.data_validation import validate_attachments, validate_recipients
from scripts.email_processor import process_email
from scripts.preview_emails import preview_emails
from scripts.utils import log_email_summary


def main():
    try:
        args = parse_arguments()
        dry_run = args.dry_run
        if dry_run:
            logger.info('Running in dry-run mode')
        if not (dry_run):
            logger.info('Starting Smart Mailer application')
        template_path = "data/email_template.txt"

        recipients, attachments = load_data()
        recipients, attachments = validate_recipients(
            recipients), validate_attachments(attachments)

        if not recipients:
            logger.error("No valid recipients found")
            raise ValueError("No valid recipients found")

        if dry_run or EMAIL_PREVIEW_ENABLED:
            preview_emails(recipients[0], template_path, attachments)

        if not dry_run:
            process_email(recipients, template_path, attachments, args)
        if dry_run:
            log_email_summary(0, len(recipients), dry_run)

    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}", exc_info=True)
        print(f"\nError in main: {e}")
        raise


if __name__ == "__main__":
    main()
