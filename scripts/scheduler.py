from datetime import datetime
import time as time_module
from config.logging import logger

# Add these color codes at the top
BLUE = '\033[94m'
END = '\033[0m'


def get_next_send_time(start_time, end_time):
    """Calculate and format the next send time"""
    current_time = datetime.now().time()
    if is_within_send_window(start_time, end_time):
        return datetime.now()
    elif current_time > end_time:
        tomorrow = datetime.combine(datetime.now().date(), start_time)
        return tomorrow.replace(day=tomorrow.day + 1)
    else:
        return datetime.combine(datetime.now().date(), start_time)


def is_within_send_window(start_time, end_time):
    """Check if current time is within allowed sending window"""
    current_time = datetime.now().time()
    return start_time <= current_time <= end_time


def wait_for_send_window(start_time, end_time):
    """Wait until next available send window if needed"""
    while not is_within_send_window(start_time, end_time):
        current_time = datetime.now().time()
        next_send: datetime = get_next_send_time(start_time, end_time)

        # Calculate time until next window
        if current_time > end_time:
            wait_seconds = (next_send - datetime.now()).total_seconds()
        else:
            wait_seconds = (next_send - datetime.now()).total_seconds()

        print(f"\n{BLUE}Next email will be sent at: {
              next_send.strftime('%Y-%m-%d %H:%M:%S')}{END}")
        logger.info(f"Outside send window ({start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}). "
                    f"Waiting {wait_seconds/3600:.1f} hours...")
        time_module.sleep(wait_seconds)
