import csv
import os

from scripts.utils import log_and_print


def load_data():
    recipients, attachments = load_recipients(
        "data/recipients.csv"), load_attachments("attachments")
    return recipients, attachments


def load_attachments(attachments_folder):
    attachments = [
        os.path.join(attachments_folder, f)
        for f in os.listdir(attachments_folder)
        if os.path.isfile(os.path.join(attachments_folder, f))
    ]
    return attachments


def load_recipients(file_path):
    recipients = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(
            (line for line in file if not line.startswith('#')))
        for row in reader:
            recipients.append({'name': row['name'], 'email': row['email']})
    return remove_duplicates(recipients)


def remove_duplicates(recipients):
    unique_recipients = []
    seen = set()

    for recipient in recipients:
        identifier = (recipient['name'], recipient['email'])

        if identifier not in seen:
            unique_recipients.append(recipient)
            seen.add(identifier)
        else:
            log_and_print(f"Skipping duplicate email and recipient pair: {
                recipient['email']} (name: {recipient['name']})", "info")
    return unique_recipients
