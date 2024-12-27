import os
import argparse
from tqdm import tqdm
from email.mime.multipart import MIMEMultipart
from scripts.csv_manager import load_recipients
from scripts.template_manager import render_template
from scripts.smtp_client import send_email
from scripts.message_builder import add_attachments
from config.settings import MAX_RETRY_ATTEMPTS

def main():
    # Add argument parser
    parser = argparse.ArgumentParser(description='Smart Mailer - Send personalized emails')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Preview emails without sending them')
    args = parser.parse_args()

    try:
        # Load data
        recipients = load_recipients("data/recipients.csv")
        template_path = "data/email_template.txt"
 
        # Define attachments folder
        attachments_folder = "attachments"
        attachments = [os.path.join(attachments_folder, f) 
                      for f in os.listdir(attachments_folder) 
                      if os.path.isfile(os.path.join(attachments_folder, f))]

        if not recipients:
            raise ValueError("No valid recipients found")

        # Process and preview/send emails
        total_sent = 0
        failed_recipients = []
        successful_attachments = set()
        all_skipped_attachments = set()

        with tqdm(total=len(recipients), desc="Sending emails") as pbar:
            for recipient in recipients:
                subject, email_content = render_template(template_path, recipient)
                
                if args.dry_run:
                    print("\n" + "="*50)
                    print(f"Preview email to: {recipient['email']}")
                    print(f"Subject: {subject}")
                    print("-"*50)
                    print(email_content)
                    sent_attachments, skipped = add_attachments(MIMEMultipart(), attachments)
                    print(f"\nAttachments: {[os.path.basename(a) for a in sent_attachments]}")
                    successful_attachments.update(sent_attachments)
                    all_skipped_attachments.update(skipped)
                    print("="*50)
                    pbar.update(1)
                else:
                    pbar.set_description(f"Sending to {recipient['email']}")
                    success, attach_result = send_email(recipient["email"], subject, email_content, attachments)
                    if success:
                        total_sent += 1
                        sent_attachments, skipped = attach_result
                        successful_attachments.update(str(a) for a in sent_attachments)
                        all_skipped_attachments.update(skipped)
                    else:
                        failed_recipients.append(recipient['email'])
                    pbar.update(1)

        if not args.dry_run:
            print(f"\nSummary: Successfully sent {total_sent}/{len(recipients)} emails")
            if failed_recipients:
                print(f"\nFailed recipients after {MAX_RETRY_ATTEMPTS} retries:")
                for email in failed_recipients:
                    print(f"- {email}")
            if successful_attachments:
                print("\nAttachments sent:")
                for attachment in successful_attachments:
                    print(f"- {os.path.basename(attachment)}")
            if all_skipped_attachments:
                print("\nAttachments that were not sent and reasons:")
                for attachment, reason in all_skipped_attachments:
                    print(f"- {os.path.basename(attachment)}: {reason}")
                print("\nPlease check the attachments folder or update the config/settings.py accordingly.")
        else:
            print(f"\nSummary: Previewed {len(recipients)} emails")
            if successful_attachments:
                print("\nAttachments that would be sent:")
                for attachment in successful_attachments:
                    print(f"- {os.path.basename(attachment)}")
            if all_skipped_attachments:
                print("\nAttachments that would not be sent and reasons:")
                for attachment, reason in all_skipped_attachments:
                    print(f"- {os.path.basename(attachment)}: {reason}")
                print("\nPlease check the attachments folder or update the config/settings.py accordingly.")

    except Exception as e:
        print(f"\nError in main: {e}")
        raise

if __name__ == "__main__":
    main()