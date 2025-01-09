import argparse
from datetime import datetime, time


def parse_time(time_str):
    try:
        return datetime.strptime(time_str, '%H:%M').time()
    except ValueError:
        raise argparse.ArgumentTypeError('Time must be in HH:MM format')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Smart Mailer - Send personalized emails')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview emails without sending them')
    parser.add_argument('--start-time', type=parse_time,
                        help='Start time for sending emails (HH:MM format)')
    parser.add_argument('--end-time', type=parse_time,
                        help='End time for sending emails (HH:MM format)')
    return parser.parse_args()
