import cv2
import os

from detection.person_detector import detect_persons
from detection.fire_detector import detect_fire_and_smoke
from detection.fall_detector import detect_fall
from detection.restricted_zone import check_restricted_zone

from risk.risk_assessment import assess_risk

from alerts.alert_manager import capture_event
from alerts.event_logger import log_event

from monitoring.event_tracker import EventTracker
from monitoring.status_manager import update_status

from agent.incident_agent import IncidentAgent

from config.settings import (
    CAMERA_INDEX,
    ZONE_X1,
    ZONE_Y1,
    ZONE_X2,
    ZONE_Y2,
    CONFIRMATION_FRAMES
)


# CONFIGURATION

STOP_FILE = "outputs/stop.flag"


# INITIALIZATION

if os.path.exists(STOP_FILE):
    os.remove(STOP_FILE)


camera = cv2.VideoCapture(
    CAMERA_INDEX
)


if not camera.isOpened():

    print(
        "Error: Could not access camera."
    )

    exit()


event_tracker = EventTracker(
    required_frames=CONFIRMATION_FRAMES
)


incident_agent = IncidentAgent()


# MAIN LOOP

while True:

    # STOP COMMAND

    if os.path.exists(STOP_FILE):

        print(
            "Stop command received."
        )

        break


    # READ CAMERA

    success, frame = camera.read()


    if not success:

        print(
            "Error: Could not read camera frame."
        )

        break


    # 1. COMPUTER VISION PERCEPTION

    person_boxes, object_results = detect_persons(
        frame
    )


    (
        fire_detected,
        smoke_detected,
        fire_results
    ) = detect_fire_and_smoke(
        frame
    )


    (
        fall_detected,
        pose_results
    ) = detect_fall(
        frame
    )


    restricted_breach = check_restricted_zone(
        person_boxes
    )


    # 2. RISK ASSESSMENT

    (
        raw_status,
        raw_status_color,
        event_name,
        risk_level,
        reason
    ) = assess_risk(
        restricted_breach,
        fall_detected,
        fire_detected,
        smoke_detected,
        person_boxes
    )


    update_status(
        status=raw_status,
        risk_level=risk_level,
        event=event_name,
        reason=reason
    )


    # 3. TEMPORAL CONFIRMATION

    confirmed = event_tracker.update(
        event_name,
        event_name != "SAFE"
    )


    # 4. INCIDENT AGENT

    agent_decision = None


    if confirmed:

        event = {

            "fire":
                bool(fire_detected),

            "smoke":
                bool(smoke_detected),

            "person":
                len(person_boxes) > 0,

            "fall":
                bool(fall_detected),

            "restricted":
                bool(restricted_breach),

            "person_at_risk": (
                len(person_boxes) > 0
                and
                (
                    bool(fire_detected)
                    or
                    bool(fall_detected)
                    or
                    bool(restricted_breach)
                )
            )
        }


        # AGENT REASONS OVER CONFIRMED EVENT

        agent_decision = (
            incident_agent.process_event(
                event
            )
        )


        # Agent-selected severity
        risk_level = (
            agent_decision["severity"]
        )


    elif event_name == "SAFE":

        incident_agent.resolve_incident()


    # 5. FINAL STATUS

    if event_name == "SAFE":

        status = "STATUS: SAFE"

        status_color = (0, 255, 0)


    elif confirmed:

        status = (
            f"AGENT: "
            f"{agent_decision['severity']}"
        )

        status_color = raw_status_color


    else:

        status = (
            "VERIFYING: "
            + raw_status
        )

        status_color = (0, 165, 255)


    # 6. DRAW DETECTIONS

    output = object_results[0].plot()


    output = fire_results[0].plot(
        img=output
    )


    output = pose_results[0].plot(
        img=output
    )


    # 7. RESTRICTED ZONE

    zone_color = (255, 165, 0)


    if restricted_breach:

        zone_color = (0, 0, 255)


    cv2.rectangle(
        output,
        (ZONE_X1, ZONE_Y1),
        (ZONE_X2, ZONE_Y2),
        zone_color,
        3
    )


    cv2.putText(
        output,
        "RESTRICTED ZONE",
        (ZONE_X1, ZONE_Y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        zone_color,
        2
    )


    # 8. EXECUTE AGENT ACTIONS

    if confirmed and agent_decision is not None:

        actions = agent_decision.get(
            "actions",
            []
        )


        # AGENT REQUESTED EVIDENCE

        if "CAPTURE_EVIDENCE" in actions:

            screenshot = capture_event(
                output,
                event_name
            )

        else:

            screenshot = None


        # LOG CONFIRMED INCIDENT

        if "LOG_EVENT" in actions:
            
            log_event(
                event_name,
                risk_level,
                reason,
                screenshot,
                agent_decision
            )


        # CONSOLE OUTPUT

        print()
        print(
            "================================"
        )

        print(
            "🚨 CONFIRMED INCIDENT"
        )

        print(
            f"Event: {event_name}"
        )

        print(
            f"Risk: {risk_level}"
        )

        print(
            f"Reason: {reason}"
        )


        if screenshot is not None:

            print(
                f"Evidence: {screenshot}"
            )


        print(
            "--------------------------------"
        )

        print(
            "🤖 INCIDENT AGENT"
        )

        print(
            f"Incident ID: "
            f"{agent_decision['incident_id']}"
        )

        print(
            f"Incident Type: "
            f"{agent_decision['incident_type']}"
        )

        print(
            f"Risk Score: "
            f"{agent_decision['risk_score']}/100"
        )

        print(
            f"Severity: "
            f"{agent_decision['severity']}"
        )


        print(
            "Risk Factors:"
        )


        for factor in agent_decision[
            "factors"
        ]:

            print(
                f"  • {factor}"
            )


        print(
            "Agent Actions:"
        )


        for action in actions:

            print(
                f"  • {action}"
            )


        print(
            "Decision: "
            f"{agent_decision['message']}"
        )


        print(
            "================================"
        )

        print()


    # 9. DISPLAY STATUS

    cv2.putText(
        output,
        status,
        (20, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        status_color,
        3
    )


    # 10. DISPLAY RISK

    if confirmed:

        cv2.putText(
            output,
            f"Risk Level: {risk_level}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            status_color,
            2
        )


    # 11. DISPLAY AGENT INFORMATION

    if agent_decision is not None:

        cv2.putText(
            output,
            (
                "Agent Risk: "
                f"{agent_decision['risk_score']}/100"
            ),
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.60,
            status_color,
            2
        )


        cv2.putText(
            output,
            (
                "Incident: "
                f"{agent_decision['incident_type']}"
            ),
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            status_color,
            2
        )


    # 12. SAVE LATEST FRAME

    cv2.imwrite(
        "outputs/latest_frame.jpg",
        output
    )


    # 13. DISPLAY CAMERA

    cv2.imshow(
        "DangerSense - AI CCTV",
        output
    )


    # 14. EXIT

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# CLEANUP

camera.release()

cv2.destroyAllWindows()