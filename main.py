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

from config.settings import (
    CAMERA_INDEX,
    ZONE_X1,
    ZONE_Y1,
    ZONE_X2,
    ZONE_Y2,
    CONFIRMATION_FRAMES
)
STOP_FILE = "outputs/stop.flag"
# INITIALIZATION

# Remove any previous stop signal
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


# Temporal event tracker
event_tracker = EventTracker(
    required_frames=CONFIRMATION_FRAMES
)

# MAIN LOOP


while True:

    if os.path.exists(STOP_FILE):
        print("Stop command received.")
        break

    success, frame = camera.read()


    if not success:

        print(
            "Error: Could not read camera frame."
        )

        break


    # DETECTION

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


    # RISK ASSESSMENT

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


    # TEMPORAL CONFIRMATION


    confirmed = event_tracker.update(
        event_name,
        event_name != "SAFE"
    )


    # FINAL STATUS

    if event_name == "SAFE":

        status = "STATUS: SAFE"

        status_color = (0, 255, 0)


    elif confirmed:

        status = raw_status

        status_color = raw_status_color


    else:

        status = "VERIFYING: " + raw_status

        status_color = (0, 165, 255)


    # DRAW DETECTIONS

    output = object_results[0].plot()


    output = fire_results[0].plot(
        img=output
    )


    output = pose_results[0].plot(
        img=output
    )


    # DRAW RESTRICTED ZONE

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


    # LOG CONFIRMED EVENT

    if confirmed:

        screenshot = capture_event(
        output,
        event_name
        )

        if screenshot is not None:

            log_event(
                event_name,
                risk_level,
                reason,
                screenshot
            )


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
            print(
                f"Evidence: {screenshot}"
            )
            print(
                "================================"
            )
            print()


    # DISPLAY STATUS

    cv2.putText(
        output,
        status,
        (20, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        status_color,
        3
    )


    # DISPLAY RISK INFORMATION

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

    
    # Save latest processed frame
    

    cv2.imwrite(
    "outputs/latest_frame.jpg",
    output
    )




    # DISPLAY CAMERA

    cv2.imshow(
        "DangerSense - AI CCTV",
        output
    )


    # EXIT

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break



# CLEANUP


camera.release()

cv2.destroyAllWindows()