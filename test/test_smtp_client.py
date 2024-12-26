import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock
from scripts.smtp_client import send_email

class TestSMTPClient(unittest.TestCase):

    @patch('scripts.smtp_client.get_credentials')
    @patch('scripts.smtp_client.build')
    def test_send_email_success(self, mock_build, mock_get_credentials):
        # Mock the credentials and Gmail API service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_get_credentials.return_value = MagicMock()

        # Mock the send method
        mock_send = mock_service.users().messages().send
        mock_send.return_value.execute.return_value = {'id': '12345'}

        # Call the send_email function
        result = send_email('test@example.com', 'Test Subject', 'Test Content', [])

        # Assertions
        self.assertTrue(result)
        mock_send.assert_called_once()
        args, kwargs = mock_send.call_args
        self.assertEqual(kwargs['userId'], 'me')
        self.assertIn('raw', kwargs['body'])

    @patch('scripts.smtp_client.get_credentials')
    @patch('scripts.smtp_client.build')
    def test_send_email_failure(self, mock_build, mock_get_credentials):
        # Mock the credentials and Gmail API service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_get_credentials.return_value = MagicMock()

        # Mock the send method to raise an exception
        mock_send = mock_service.users().messages().send
        mock_send.side_effect = Exception('Failed to send email')

        # Call the send_email function
        result = send_email('test@example.com', 'Test Subject', 'Test Content', [])

        # Assertions
        self.assertFalse(result)
        mock_send.assert_called_once()

    @patch('scripts.smtp_client.get_credentials')
    @patch('scripts.smtp_client.build')
    def test_send_email_with_attachments(self, mock_build, mock_get_credentials):
        # Mock the credentials and Gmail API service
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        mock_get_credentials.return_value = MagicMock()

        # Mock the send method
        mock_send = mock_service.users().messages().send
        mock_send.return_value.execute.return_value = {'id': '12345'}

        # Create a temporary file to use as an attachment
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"Test attachment content")
            tmp_file_path = tmp_file.name

        try:
            # Call the send_email function with the attachment
            result = send_email('test@example.com', 'Test Subject', 'Test Content', [tmp_file_path])

            # Assertions
            self.assertTrue(result)
            mock_send.assert_called_once()
            args, kwargs = mock_send.call_args
            self.assertEqual(kwargs['userId'], 'me')
            self.assertIn('raw', kwargs['body'])
        finally:
            os.remove(tmp_file_path)

if __name__ == "__main__":
    unittest.main()