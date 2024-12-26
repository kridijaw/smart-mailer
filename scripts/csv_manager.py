import csv
from scripts.validate_email import validate_email

def load_recipients(file_path):
    recipients = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if validate_email(row["email"]):
                recipients.append({"name": row["name"], "email": row["email"]})
            else:
                print(f"Invalid email: {row['email']}")
    return recipients