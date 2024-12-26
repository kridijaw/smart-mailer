import os
from scripts.csv_manager import load_recipients
from scripts.template_manager import render_template
from scripts.smtp_client import send_email

def main():
    try:
        # Load data
        recipients = load_recipients("data/recipients.csv")
        template_path = "data/email_template.txt"
 
        # Define attachments folder
        attachments_folder = "attachments"
        attachments = [os.path.join(attachments_folder, f) for f in os.listdir(attachments_folder) if os.path.isfile(os.path.join(attachments_folder, f))]

        if not recipients:
            raise ValueError("No valid recipients found")

        # Process and send emails
        for recipient in recipients:
            subject, email_content = render_template(template_path, recipient)
            send_email(recipient["email"], subject, email_content, attachments)

    except Exception as e:
        print(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    main()