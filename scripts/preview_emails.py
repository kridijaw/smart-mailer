import markdown
import os
import webbrowser

from datetime import datetime
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
    return subject, email_content, reply_to


def save_as_html(email_details, recipient):
    output_path = os.path.join('logs', f'rendered_email_{
                               datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
    with open(output_path, 'w') as f:
        html_content = markdown.markdown(email_details[1])
        complete_html = add_html_boilerplate(
            email_details[0], html_content, email_details[2], recipient)
        f.write(complete_html)

    webbrowser.open(f'file://{os.path.abspath(output_path)}')


def add_html_boilerplate(subject, html_content, reply_to, recipient):
    reply_to_html = f"<p>Reply-To: {reply_to}</p>" if reply_to else ""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Email Preview</title>
    </head>
    <body>
        <h2>Subject: {subject}</h2>
        <p>To: {recipient['email']}</p>
        {reply_to_html}
        <hr>
        {html_content}
    </body>
    </html>
    """
