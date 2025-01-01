import os
from email.mime.multipart import MIMEMultipart
from scripts.template_manager import render_template
from scripts.message_builder import add_attachments


def preview_emails(recipient, template_path, attachments):
    subject, email_content = render_template(template_path, recipient)

    print("\n" + "="*50)
    print(f"Preview email to: {recipient['email']}")
    print(f"Subject: {subject}")
    print("-"*50)
    print(email_content)
    sent_attachments, skipped_attachments, ignored_attachments = add_attachments(
        MIMEMultipart(), attachments)
    print(f"\nAttachments: {[os.path.basename(a)
          for a in sent_attachments]}")
    print("="*50)
