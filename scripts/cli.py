import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Smart Mailer - Send personalized emails')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Preview emails without sending them')
    return parser.parse_args()
