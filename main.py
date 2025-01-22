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
        dry_run = setup_config(args)
        template_path = "data/email_template.txt"

        # Load and validate data
        recipients, attachments = load_data()
        recipients = validate_recipients(recipients)
        attachments = validate_attachments(attachments)

        # Preview mode
        if dry_run or EMAIL_PREVIEW_ENABLED:
            preview_emails(recipients[0], template_path, attachments)
            if dry_run:
                log_email_summary(0, len(recipients), dry_run)
                return

        # Process emails
        process_email(recipients, template_path, attachments, args)

    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}", exc_info=True)
        print(f"\nError in main: {e}")
        raise


def setup_config(args):
    """Initialize configuration settings"""
    if args.dry_run:
        logger.info('Running in dry-run mode')
    else:
        logger.info('Starting Smart Mailer application')
    return args.dry_run


if __name__ == "__main__":
    main()
