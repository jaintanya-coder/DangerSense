import json
import os
from datetime import datetime

from config.settings import EVENT_LOG_FILE


def log_event(
    event_name,
    risk_level,
    reason,
    screenshot=None,
    agent_decision=None
):

    """
    Save a confirmed safety event to events.json.

    agent_decision contains the contextual decision
    produced by the Incident Agent.
    """

    log_folder = os.path.dirname(
        EVENT_LOG_FILE
    )


    os.makedirs(
        log_folder,
        exist_ok=True
    )


    # ========================================================
    # LOAD EXISTING EVENTS
    # ========================================================

    if os.path.exists(
        EVENT_LOG_FILE
    ):

        try:

            with open(
                EVENT_LOG_FILE,
                "r"
            ) as file:

                events = json.load(
                    file
                )

        except (
            json.JSONDecodeError,
            FileNotFoundError
        ):

            events = []

    else:

        events = []


    # ========================================================
    # BASE EVENT RECORD
    # ========================================================

    event = {

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "event":
            event_name,

        "risk_level":
            risk_level,

        "reason":
            reason,

        "screenshot":
            screenshot
    }


    # ========================================================
    # ADD AGENT DECISION
    # ========================================================

    if agent_decision is not None:

        event["incident_id"] = (
            agent_decision.get(
                "incident_id"
            )
        )

        event["incident_type"] = (
            agent_decision.get(
                "incident_type"
            )
        )

        event["risk_score"] = (
            agent_decision.get(
                "risk_score"
            )
        )

        event["agent_severity"] = (
            agent_decision.get(
                "severity"
            )
        )

        event["risk_factors"] = (
            agent_decision.get(
                "factors",
                []
            )
        )

        event["agent_actions"] = (
            agent_decision.get(
                "actions",
                []
            )
        )

        event["agent_message"] = (
            agent_decision.get(
                "message"
            )
        )

        event["incident_status"] = (
            agent_decision.get(
                "status"
            )
        )


    # ========================================================
    # SAVE EVENT
    # ========================================================

    events.append(
        event
    )


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
        f"[EVENT LOGGED] "
        f"{event_name} | {risk_level}"
    )