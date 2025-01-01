from config.logging import logger
from config.settings import PREVIEW_EMAIL
from scripts.attachment_utils import check_attachments
from scripts.cli import parse_arguments
from scripts.email_processor import process_recipients
from scripts.preview_emails import preview_emails
from scripts.utils import load_data


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
