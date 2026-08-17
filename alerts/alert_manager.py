import os
import cv2
from datetime import datetime, timedelta

from config.settings import SCREENSHOT_FOLDER


# SCREENSHOT COOLDOWN

# Prevent the same type of event from generating
# screenshots repeatedly within a short period.

SCREENSHOT_COOLDOWN_SECONDS = 60

last_screenshot_time = {}


# CAPTURE EVENT

def capture_event(output, event_name):
    """
    Save a screenshot of a confirmed safety event.

    The same event type cannot create another screenshot
    during the cooldown period.

    Returns:
        Path of saved screenshot if captured.
        None if screenshot is skipped because of cooldown.
    """

    now = datetime.now()


    # Check previous screenshot

    previous_time = last_screenshot_time.get(
        event_name
    )


    if previous_time is not None:

        elapsed_time = (
            now - previous_time
        ).total_seconds()


        if elapsed_time < SCREENSHOT_COOLDOWN_SECONDS:

            return None


    # Create screenshot folder

    os.makedirs(
        SCREENSHOT_FOLDER,
        exist_ok=True
    )


    # Generate filename

    timestamp = now.strftime(
        "%Y%m%d_%H%M%S"
    )


    filename = os.path.join(
        SCREENSHOT_FOLDER,
        f"{event_name.lower()}_{timestamp}.jpg"
    )


    # Save screenshot

    cv2.imwrite(
        filename,
        output
    )


    # Remember when screenshot was created
    last_screenshot_time[event_name] = now


    return filename