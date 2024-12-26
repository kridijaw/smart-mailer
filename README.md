# Smart Mailer

A secure Python application for sending personalized emails using Gmail API with OAuth 2.0 authentication.

## Prerequisites

- Python 3.8 or higher
- A Google Cloud Platform account with Gmail API enabled
- OAuth 2.0 credentials from Google Cloud Console

## Installation

1. Clone the repository
2. Install dependencies:

```sh
pip install -r requirements.txt
```

## Configuration

1. Create a project in the Google Cloud Console
2. Enable the Gmail API
3. Create OAuth 2.0 credentials
4. Download the credentials and save as credentials.json in the project root

## File Structure

- [`email_template.txt`](data/email_template.txt): Template for your email content using Jinja2 syntax
- [`recipients.csv`](data/recipients.csv): CSV file containing recipient information (email, name)
- scripts: Core functionality modules
- [`config.py`](config.py): OAuth configuration
- [`main.py`](main.py): Main application entry point

## Usage

1. Prepare your recipients list in recipients.csv:

```csv
email,name
example@email.com,John
another@email.com,Jane
```

2. Create your email template in email_template.txt:

```txt
---
subject: Your Email Subject Here
---
Hi {{ name }},

Your personalized message here.

Best regards,
Your Name
```

3. Run the application:

```sh
py
```

On first run, your browser will open for Google authentication.

## Security Features

- OAuth 2.0 authentication with Gmail API
- Email validation
- Template content sanitization
- Secure credential storage

## Important Security Notes

- Keep your credentials.json and token.json files secure
- Never commit these files to version control
- Add them to your [.gitignore](.gitignore) file

## Files to protect

The following files contain sensitive information and should not be shared:

- credentials.json
- token.json

## Error Handling

The application includes comprehensive error handling for:

- Invalid email addresses
- Template rendering issues
- Email sending failures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.