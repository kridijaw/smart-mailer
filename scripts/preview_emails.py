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

    sent_attachments = []
    if attachments:
        sent_attachments = add_attachments(
            MIMEMultipart(), attachments)
        print(f"\nAttachments: {[os.path.basename(a)
                                 for a in sent_attachments]}")
    else:
        print("\n(No attachments included)")
    print("="*49)
    return subject, email_content, reply_to, sent_attachments


def save_as_html(email_details, recipient):
    output_path = os.path.join('logs', f'rendered_email_{
                               datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
    with open(output_path, 'w') as f:
        html_content = markdown.markdown(email_details[1])
        complete_html = add_html_boilerplate(
            email_details[0], html_content, email_details[2], email_details[3], recipient)
        f.write(complete_html)

    webbrowser.open(f'file://{os.path.abspath(output_path)}')


def add_html_boilerplate(subject, html_content, reply_to, sent_attachments, recipient):
    reply_to_html = f"<p>Reply-To: {reply_to}</p>" if reply_to else ""
    attachments_html = ""
    # if 'attachments' in recipient and recipient['attachments']:
    if sent_attachments:
        attachments_html = add_html_attachment(sent_attachments)

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
      {attachments_html}
    </body>
    </html>
    """


def add_html_attachment(attachments):
    FILE_TYPES = {
        'pdf': {
            'extensions': ('.pdf',),
            'template': lambda f, n: f'<a href="{f}" target="_blank">{n}</a>'
        },
        'image': {
            'extensions': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'),
            'template': lambda f, n: f'<img src="{f}" alt="{n}">'
        },
        'video': {
            'extensions': ('.mp4', '.webm', '.ogg', '.mov', '.avi'),
            'template': lambda f, n: f'''<video controls>
                <source src="{f}" type="video/{n.split('.')[-1]}">
                Your browser does not support the video tag.
            </video>'''
        },
        'audio': {
            'extensions': ('.mp3', '.wav', '.ogg', '.m4a', 'flac'),
            'template': lambda f, n: f'''<audio controls>
                <source src="{f}" type="audio/{n.split('.')[-1]}">
                Your browser does not support the audio element.
            </audio>'''
        },
        'text': {
            'extensions': ('.txt', '.md', '.csv', '.json'),
            'template': lambda f, n: f'<a href="{f}" target="_blank">{n} (Text File)</a>'
        }
    }

    def get_file_type(filename):
        filename_lower = filename.lower()
        for file_type, info in FILE_TYPES.items():
            if filename_lower.endswith(info['extensions']):
                return file_type
        return 'default'

    attachments_html = "<hr>\n<h3>Attachments</h3>"

    for attachment in attachments:
        clean_name = attachment.replace("attachments/", "")
        file_path = f"../attachments/{clean_name}"

        file_type = get_file_type(clean_name)
        if file_type in FILE_TYPES:
            template = FILE_TYPES[file_type]['template']
            attachments_html += f"\n{template(file_path, clean_name)}"
        else:
            attachments_html += f'\n<a href="{
                file_path}" download>{clean_name} (Download)</a>'

        attachments_html += '<br>'

    return attachments_html
