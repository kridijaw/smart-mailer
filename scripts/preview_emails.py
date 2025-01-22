import os
from email.mime.multipart import MIMEMultipart
from scripts.template_manager import render_template
from scripts.message_builder import add_attachments


def preview_emails(recipient, template_path, attachments):
    subject, email_content, reply_to = render_template(
        template_path, recipient)
    print("\n" + "="*21 + "PREVIEW" + "="*21)
    print(f"Subject: {subject}")
    print(f"To: {recipient['email']}")
    if (reply_to):
        print(f"Reply-To: {reply_to}")
    print("-"*49)
    print(email_content)
    if attachments:
        sent_attachments = []
        sent_attachments = add_attachments(
            MIMEMultipart(), attachments)
        print(f"\nAttachments: {[os.path.basename(a)
                                 for a in sent_attachments]}")
    else:
        print("\n(No attachments included)")
    print("="*49)
