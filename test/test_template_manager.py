import unittest
import tempfile
import os
from scripts.csv_manager import load_recipients

class TestCSVManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up temporary files
        for filename in os.listdir(self.test_dir):
            file_path = os.path.join(self.test_dir, filename)
            os.remove(file_path)
        os.rmdir(self.test_dir)

    def create_temp_csv(self, content):
        # Helper function to create a temporary CSV file
        temp_csv_path = os.path.join(self.test_dir, 'test_recipients.csv')
        with open(temp_csv_path, 'w') as temp_csv:
            temp_csv.write(content)
        return temp_csv_path

    def test_load_recipients_valid(self):
        csv_content = "email,name\nvalid@example.com,Valid User\nanother.valid@example.com,Another User"
        temp_csv_path = self.create_temp_csv(csv_content)
        recipients = load_recipients(temp_csv_path)
        self.assertEqual(len(recipients), 2)
        self.assertEqual(recipients[0]['email'], 'valid@example.com')
        self.assertEqual(recipients[0]['name'], 'Valid User')
        self.assertEqual(recipients[1]['email'], 'another.valid@example.com')
        self.assertEqual(recipients[1]['name'], 'Another User')

    def test_load_recipients_invalid_email(self):
        csv_content = "email,name\ninvalid-email,Invalid User\nvalid@example.com,Valid User"
        temp_csv_path = self.create_temp_csv(csv_content)
        recipients = load_recipients(temp_csv_path)
        self.assertEqual(len(recipients), 1)
        self.assertEqual(recipients[0]['email'], 'valid@example.com')
        self.assertEqual(recipients[0]['name'], 'Valid User')

    def test_load_recipients_empty_file(self):
        csv_content = ""
        temp_csv_path = self.create_temp_csv(csv_content)
        recipients = load_recipients(temp_csv_path)
        self.assertEqual(len(recipients), 0)

    def test_load_recipients_missing_columns(self):
        csv_content = "email\nvalid@example.com\nanother.valid@example.com"
        temp_csv_path = self.create_temp_csv(csv_content)
        with self.assertRaises(KeyError):
            load_recipients(temp_csv_path)

if __name__ == "__main__":
    unittest.main()