import os
import tempfile
import unittest
from email.mime.multipart import MIMEMultipart
from scripts.message_builder import create_base_message, create_content_parts, add_attachments

class TestMessageBuilder(unittest.TestCase):

    def test_create_content_parts(self):
        content = "**Bold** and *italic*"
        text_part, html_part = create_content_parts(content)
        self.assertIn("<strong>Bold</strong>", html_part.get_payload())
        self.assertIn("Bold", text_part.get_payload())
        self.assertIn("<em>italic</em>", html_part.get_payload())
        self.assertIn("italic", text_part.get_payload())

    def test_create_base_message(self):
        to_email = "test@example.com"
        subject = "Test Subject"
        message = create_base_message(to_email, subject)
        self.assertIsInstance(message, MIMEMultipart)
        self.assertEqual(message['to'], to_email)
        self.assertEqual(message['subject'], subject)

    def test_add_attachments(self):
        message = MIMEMultipart()
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"Test attachment content")
            tmp_file_path = tmp_file.name

        try:
            add_attachments(message, [tmp_file_path])
            self.assertGreater(len(message.get_payload()), 0)
            attachment = message.get_payload()[-1]
            self.assertEqual(attachment.get_filename(), os.path.basename(tmp_file_path))
            self.assertEqual(attachment.get_payload(decode=True), b"Test attachment content")
        finally:
            os.remove(tmp_file_path)

    def test_add_attachments_nonexistent_file(self):
        message = MIMEMultipart()
        add_attachments(message, ["nonexistent_file.txt"])
        self.assertEqual(len(message.get_payload()), 0)

    def test_add_attachments_empty_list(self):
        message = MIMEMultipart()
        add_attachments(message, [])
        self.assertEqual(len(message.get_payload()), 0)

    def test_add_multiple_attachments(self):
        message = MIMEMultipart()
        tmp_files = []
        try:
            for i in range(2):
                tmp_file = tempfile.NamedTemporaryFile(delete=False)
                tmp_file.write(f"Test attachment content {i}".encode())
                tmp_file_path = tmp_file.name
                tmp_files.append(tmp_file_path)
                tmp_file.close()

            add_attachments(message, tmp_files)
            attachments = [part for part in message.get_payload() if part.get_content_disposition() == 'attachment']
            self.assertEqual(len(attachments), 2)  # Expecting 2 attachments
            for i, tmp_file_path in enumerate(tmp_files):
                attachment = attachments[i]
                self.assertEqual(attachment.get_filename(), os.path.basename(tmp_file_path))
                self.assertEqual(attachment.get_payload(decode=True), f"Test attachment content {i}".encode())
        finally:
            for tmp_file_path in tmp_files:
                os.remove(tmp_file_path)

    def test_add_invalid_attachment_type(self):
        message = MIMEMultipart()
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(b"Test attachment content")
            tmp_file_path = tmp_file.name

        try:
            # Rename the file to an unsupported type
            invalid_file_path = tmp_file_path + ".unsupported"
            os.rename(tmp_file_path, invalid_file_path)
            add_attachments(message, [invalid_file_path])
            self.assertGreater(len(message.get_payload()), 0)
            attachment = message.get_payload()[-1]
            self.assertEqual(attachment.get_filename(), os.path.basename(invalid_file_path))
            self.assertEqual(attachment.get_payload(decode=True), b"Test attachment content")
        finally:
            os.remove(invalid_file_path)

if __name__ == "__main__":
    unittest.main()