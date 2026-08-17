def get_response_policy(severity):

    policies = {

        "LOW": {
            "actions": [
                "LOG_EVENT"
            ],
            "message":
                "Low-risk event detected."
        },

        "MEDIUM": {
            "actions": [
                "LOG_EVENT",
                "CAPTURE_EVIDENCE"
            ],
            "message":
                "Potential hazard detected. Monitoring continues."
        },

        "HIGH": {
            "actions": [
                "LOG_EVENT",
                "CAPTURE_EVIDENCE",
                "GENERATE_ALERT",
                "CONTINUE_MONITORING"
            ],
            "message":
                "High-risk incident detected."
        },

        "CRITICAL": {
            "actions": [
                "LOG_EVENT",
                "CAPTURE_EVIDENCE",
                "GENERATE_ALERT",
                "CONTINUE_MONITORING",
                "ESCALATE"
            ],
            "message":
                "Critical incident detected. Immediate attention required."
        }
    }

    return policies.get(
        severity,
        policies["LOW"]
    )