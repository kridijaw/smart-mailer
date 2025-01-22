from datetime import datetime
import time as time_module
from config.settings import EMAIL_SCHEDULING_ENABLED, SEND_TIME_START, SEND_TIME_END
from config.logging import logger

# Add these color codes at the top
BLUE = '\033[94m'
END = '\033[0m'


def get_next_send_time():
    """Calculate and format the next send time"""
    current_time = datetime.now().time()
    if is_within_send_window():
        return datetime.now()
    elif current_time > SEND_TIME_END:
        tomorrow = datetime.combine(datetime.now().date(), SEND_TIME_START)
        return tomorrow.replace(day=tomorrow.day + 1)
    else:
        return datetime.combine(datetime.now().date(), SEND_TIME_START)


def is_within_send_window():
    """Check if current time is within allowed sending window"""
    if not EMAIL_SCHEDULING_ENABLED:
        return True

    current_time = datetime.now().time()
    return SEND_TIME_START <= current_time <= SEND_TIME_END


def wait_for_send_window():
    """Wait until next available send window if needed"""
    while not is_within_send_window():
        current_time = datetime.now().time()
        next_send = get_next_send_time()

        # Calculate time until next window
        if current_time > SEND_TIME_END:
            wait_seconds = (next_send - datetime.now()).total_seconds()
        else:
            wait_seconds = (next_send - datetime.now()).total_seconds()

        print(f"\n{BLUE}Next email will be sent at: {
              next_send.strftime('%Y-%m-%d %H:%M:%S')}{END}")
        logger.info(f"Outside send window ({SEND_TIME_START.strftime('%H:%M')} - {SEND_TIME_END.strftime('%H:%M')}). "
                    f"Waiting {wait_seconds/3600:.1f} hours...")
        time_module.sleep(wait_seconds)
