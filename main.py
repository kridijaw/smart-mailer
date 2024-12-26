import os
import argparse
from scripts.csv_manager import load_recipients
from scripts.template_manager import render_template
from scripts.smtp_client import send_email

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
        for recipient in recipients:
            subject, email_content = render_template(template_path, recipient)
            
            if args.dry_run:
                print("\n" + "="*50)
                print(f"Preview email to: {recipient['email']}")
                print(f"Subject: {subject}")
                print("-"*50)
                print(email_content)
                print(f"\nAttachments: {[os.path.basename(a) for a in attachments]}")
                print("="*50)
            else:
                send_email(recipient["email"], subject, email_content, attachments)

    except Exception as e:
        print(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    main()