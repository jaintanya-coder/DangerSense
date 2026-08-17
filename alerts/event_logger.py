import json
import os
from datetime import datetime
from config.settings import EVENT_LOG_FILE


def log_event(
    event_name,
    risk_level,
    reason,
    screenshot=None
):
    """
    Save a confirmed safety event to events.json.
    """

    log_folder = os.path.dirname(
        EVENT_LOG_FILE
    )

    os.makedirs(
        log_folder,
        exist_ok=True
    )


    # Load existing events
    if os.path.exists(EVENT_LOG_FILE):

        try:

            with open(
                EVENT_LOG_FILE,
                "r"
            ) as file:

                events = json.load(file)

        except (json.JSONDecodeError, FileNotFoundError):

            events = []

    else:

        events = []


    # Create event record
    event = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "event": event_name,

        "risk_level": risk_level,

        "reason": reason,

        "screenshot": screenshot
    }


    events.append(event)


    
    with open(
        EVENT_LOG_FILE,
        "w"
    ) as file:

        json.dump(
            events,
            file,
            indent=4
        )


    print(
        f"[EVENT LOGGED] {event_name} | {risk_level}"
    )