def assess_risk(
    restricted_breach,
    fall_detected,
    fire_detected,
    smoke_detected,
    person_boxes
):
    """
    Combine individual detections into a contextual
    safety incident.

    Returns:
        status
        status_color
        event_name
        risk_level
        reason
    """

    # Critical situations

    if restricted_breach and fire_detected:

        return (
            "CRITICAL: FIRE + RESTRICTED AREA",
            (0, 0, 255),
            "FIRE_RESTRICTED",
            "CRITICAL",
            "Fire detected in a restricted area."
        )


    if fire_detected and person_boxes:

        return (
            "CRITICAL: PERSON + FIRE",
            (0, 0, 255),
            "PERSON_FIRE",
            "CRITICAL",
            "Fire detected while a person is present."
        )


    if smoke_detected and person_boxes:

        return (
            "CRITICAL: PERSON + SMOKE",
            (0, 0, 255),
            "PERSON_SMOKE",
            "CRITICAL",
            "Smoke detected while a person is present."
        )


    if fall_detected:

        return (
            "HIGH RISK: POSSIBLE FALL",
            (0, 0, 255),
            "FALL",
            "HIGH",
            "Possible fall detected."
        )


    if restricted_breach:

        return (
            "ALERT: RESTRICTED AREA BREACH",
            (0, 0, 255),
            "RESTRICTED_BREACH",
            "HIGH",
            "Person entered the restricted area."
        )


    if fire_detected:

        return (
            "WARNING: FIRE DETECTED",
            (0, 165, 255),
            "FIRE",
            "HIGH",
            "Fire detected."
        )


    if smoke_detected:

        return (
            "WARNING: SMOKE DETECTED",
            (0, 165, 255),
            "SMOKE",
            "MEDIUM",
            "Smoke detected."
        )


    return (
        "STATUS: SAFE",
        (0, 255, 0),
        "SAFE",
        "SAFE",
        "No safety threats detected."
    )