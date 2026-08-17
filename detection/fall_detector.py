from ultralytics import YOLO


# Load pose model

pose_model = YOLO(
    "models/yolo11n-pose.pt"
)


# Fall detection thresholds

HORIZONTAL_RATIO = 1.6

MIN_KEYPOINT_CONFIDENCE = 0.35

MIN_BODY_HEIGHT_RATIO = 0.25


# Detect possible falls

def detect_fall(frame):

    pose_results = pose_model(
        frame,
        verbose=False
    )

    fall_detected = False


    for result in pose_results:

        if result.keypoints is None:
            continue


        # Keypoints shape:
        #
        # person
        #   ↓
        # [17 keypoints]
        #
        keypoints = result.keypoints.xy

        confidences = result.keypoints.conf


        if keypoints is None:
            continue


        for person_index in range(
            len(keypoints)
        ):

            points = keypoints[
                person_index
            ]


            confidence = confidences[
                person_index
            ]


            # Important body keypoints

            # COCO pose indexes:
            #
            # 5  = left shoulder
            # 6  = right shoulder
            # 11 = left hip
            # 12 = right hip

            left_shoulder = points[5]
            right_shoulder = points[6]

            left_hip = points[11]
            right_hip = points[12]


            # Make sure important points are visible

            important_points = [
                5,
                6,
                11,
                12
            ]


            valid_points = True


            for point_index in important_points:

                if (
                    confidence[point_index]
                    < MIN_KEYPOINT_CONFIDENCE
                ):

                    valid_points = False

                    break


            if not valid_points:

                continue


            # Calculate shoulder and hip centers

            shoulder_x = (
                left_shoulder[0]
                + right_shoulder[0]
            ) / 2


            shoulder_y = (
                left_shoulder[1]
                + right_shoulder[1]
            ) / 2


            hip_x = (
                left_hip[0]
                + right_hip[0]
            ) / 2


            hip_y = (
                left_hip[1]
                + right_hip[1]
            ) / 2


            # Body dimensions

            body_width = abs(
                shoulder_x - hip_x
            )


            body_height = abs(
                shoulder_y - hip_y
            )


            # Determine body orientation

            if body_height <= 1:

                continue


            horizontal_ratio = (
                body_width / body_height
            )


            # Detect horizontal posture

            horizontal_body = (
                horizontal_ratio
                > HORIZONTAL_RATIO
            )


            # Prevent tiny / unreliable detections

            if body_height < 20:

                continue


            # Fall condition

            if horizontal_body:

                fall_detected = True

                break


        if fall_detected:

            break


    return (
        fall_detected,
        pose_results
    )