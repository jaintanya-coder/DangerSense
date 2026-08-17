# Model paths

OBJECT_MODEL_PATH = "models/yolo11n.pt"
FIRE_MODEL_PATH = "models/best.pt"
POSE_MODEL_PATH = "models/yolo11n-pose.pt"


# Detection confidence

PERSON_CONFIDENCE = 0.40
FIRE_CONFIDENCE = 0.40


# Restricted zone

ZONE_X1 = 20
ZONE_Y1 = 30
ZONE_X2 = 320
ZONE_Y2 = 450

# Camera

CAMERA_INDEX = 0


# Output

SCREENSHOT_FOLDER = "outputs/screenshots"

# Temporal confirmation

# Number of consecutive frames required
# before an event is considered confirmed.

CONFIRMATION_FRAMES = 8


# Event logging

EVENT_LOG_FILE = "outputs/logs/events.json"

CURRENT_STATUS_FILE = "outputs/current_status.json"
LATEST_FRAME_PATH = "outputs/latest_frame.jpg"