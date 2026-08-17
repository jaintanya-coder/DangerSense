from ultralytics import YOLO

from config.settings import (
    FIRE_MODEL_PATH,
    FIRE_CONFIDENCE
)


# Load fire and smoke detection model
fire_model = YOLO(FIRE_MODEL_PATH)


def detect_fire_and_smoke(frame):
    """
    Detect fire and smoke in the given frame.

    Returns:
        fire_detected: True if fire is detected
        smoke_detected: True if smoke is detected
        results: YOLO results used for visualization
    """

    results = fire_model(
        frame,
        verbose=False
    )

    fire_detected = False
    smoke_detected = False

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            name = fire_model.names[class_id].lower()

            if confidence > FIRE_CONFIDENCE:

                if name == "fire":
                    fire_detected = True

                elif name == "smoke":
                    smoke_detected = True

    return (
        fire_detected,
        smoke_detected,
        results
    )