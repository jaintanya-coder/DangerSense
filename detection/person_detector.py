from ultralytics import YOLO

from config.settings import (
    OBJECT_MODEL_PATH,
    PERSON_CONFIDENCE
)


# Load object detection model
object_model = YOLO(OBJECT_MODEL_PATH)


def detect_persons(frame):
    """
    Detect people in the given frame.

    Returns:
        person_boxes: list of person bounding boxes
        results: YOLO results used for visualization
    """

    results = object_model(
        frame,
        verbose=False
    )

    person_boxes = []

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            name = object_model.names[class_id]

            if (
                name == "person"
                and confidence > PERSON_CONFIDENCE
            ):

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                person_boxes.append(
                    (x1, y1, x2, y2)
                )

    return person_boxes, results