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
2. Create your email template in [`email_template.txt`](data/email_template.txt). The template can be in plain text, HTML, or Markdown format. The Jinja2 expression `{{ name }}` will be replaced with the actual name of the email recipient when the template is rendered.
3. Optional: Add attachments to the `attachments` folder.
4. Adjust the configuration settings in [`config/settings.py`](config/settings.py) as needed.
5. Run the application:

```sh
# Send emails
python main.py

# Preview emails without sending (dry-run mode)
python main.py --dry-run
```

On first run, your browser will open for Google authentication.

## Security Features

- OAuth 2.0 authentication with Gmail API
- Email validation
- Template content sanitization
- Secure credential storage
- Attachment handling
  - Maximum attachment size: 50MB (configurable in `config/settings.py`)
  - Allowed MIME types: `application/pdf`, `image/*` (configurable in `config/settings.py`)

## Important Security Notes

- Keep your credentials.json and token.json files secure
- Never commit these files to version control
- Add them to your .gitignore file

## Files to protect

The following files contain sensitive information and should not be shared:

- credentials.json
- token.json

## Error Handling

The application includes comprehensive error handling for:

- Invalid email addresses
- Template rendering issues
- Email sending failures with automatic retries
  - Configurable retry attempts (default: 5)
  - Exponential backoff between retries
  - Detailed failure reporting

## Testing

The application includes comprehensive unit tests to ensure reliability and correctness. The tests cover various aspects of the application, including:

- Email validation
- Template rendering
- Attachment handling
  - MIME type restrictions
  - File size limits
- Email sending with retries

To run the tests, use the following command:

```sh
python -m unittest discover -s test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [`LICENSE file`](LICENSE) file for details.
