# Smart Mailer

A secure Python application for sending personalized emails using Gmail API with OAuth 2.0 authentication.

## Prerequisites

- Python 3.8 or higher
- A Google Cloud Platform account with Gmail API enabled
- OAuth 2.0 credentials from Google Cloud Console

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com)
2. Enable the [Gmail API](https://console.cloud.google.com/apis/library/gmail.googleapis.com)
3. Create OAuth 2.0 credentials
4. Download the credentials and save it as `credentials.json` in the project root

## File Structure

- `main.py`: Main application entry point
- `scripts`: Folder containing core functionality modules
- `attachments`: Folder containing files to be attached to all emails
- `data/email_template.txt`: Template for your email content
- `data/recipients.csv`: CSV file containing recipient information (email, name)
- `config/settings.py`: Configuration settings for the application

## Usage

1. Prepare your recipients list in [`recipients.csv`](data/recipients.csv).
2. Create your email template in [`email_template.txt`](data/email_template.txt). The template can be in plain text, HTML, or Markdown format. The Jinja2 expression `{{ name }}` will be replaced with the name of the email recipient defined in recipients.csv when the template is rendered.
3. Optional: Add attachments to the `attachments` folder.
4. Adjust the configuration settings in [`config/settings.py`](config/settings.py) as needed.
5. Run the application:

```bash
# Send emails
python main.py

# Send emails between a specific time window
python main.py --start-time 10:00 --end-time 15:00

# Preview emails without sending (dry-run mode)
python main.py --dry-run
```

On first run, your browser will open for Google authentication.

## Troubleshooting

### Token Expired Error

If you encounter this error:

```bash
Error in main: ('invalid_grant: Token has been expired or revoked.', {'error': 'invalid_grant', 'error_description': 'Token has been expired or revoked.'})
```

Solution:

1. Delete the `token.json` file in the main folder
2. Run the application again
3. Complete the Google authentication process again when prompted

## Important Security Notes

- Keep your credentials.json and token.json files secure
- Never commit these files to version control
- Add them to your .gitignore file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [`LICENSE file`](LICENSE) file for details.
