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
2. Create your email template in [`email_template.txt`](data/email_template.txt). The template can be in plain text, HTML, or Markdown format. The Jinja2 expression `{{ name }}` will be replaced with the name of the email recipient defined in recipients.csv when the template is rendered.
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

## Important Security Notes

- Keep your credentials.json and token.json files secure
- Never commit these files to version control
- Add them to your .gitignore file

## Features

### Core Features

- Personalized email sending using Gmail API
- OAuth 2.0 authentication for secure access
- Template-based emails with Jinja2 support
- CSV-based recipient management
- Bulk attachment handling
- Dry-run mode for email preview
- Attachment handling:
  - Maximum attachment size: 50MB (configurable in `config/settings.py`)
  - Allowed MIME types: `application/pdf`, `image/*` (configurable in `config/settings.py`)

### Template System

- Support for plain text, HTML, and Markdown formats
- Variable interpolation using Jinja2
- Personalization using recipient data
- Template validation and preview

### Email Scheduling

- Configurable send time windows
- Automatic schedule adherence
- CLI options for custom scheduling
- Schedule override capabilities

### Security

- OAuth 2.0 authentication with Gmail API
- Email validation
- Template content sanitization
- Secure credential storage

### Error Handling

- Automatic retry mechanism
- Configurable retry attempts
- Exponential backoff
- Detailed error reporting
- Graceful failure handling

### Testing

- Comprehensive unit test suite
- Template rendering tests
- Attachment validation tests
- Email sending tests
- Mock email preview

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
