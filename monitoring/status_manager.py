import json
import os


def update_status(
    status,
    risk_level,
    event,
    reason
):
    """
    Save the current DangerSense system status.
    """

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    current_status = {
        "status": status,
        "risk_level": risk_level,
        "event": event,
        "reason": reason
    }

    with open(
        "outputs/current_status.json",
        "w"
    ) as file:

        json.dump(
            current_status,
            file,
            indent=4
        )