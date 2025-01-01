import os

from scripts.csv_manager import load_recipients


def load_data():
    recipients = load_recipients("data/recipients.csv")
    attachments_folder = "attachments"
    attachments = [
        os.path.join(attachments_folder, f)
        for f in os.listdir(attachments_folder)
        if os.path.isfile(os.path.join(attachments_folder, f))
    ]
    return recipients, attachments
