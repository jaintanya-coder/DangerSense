import json
import os
from datetime import datetime


class ActionExecutor:

    def __init__(self):

        self.action_log = (
            "outputs/logs/agent_actions.json"
        )

        os.makedirs(
            os.path.dirname(self.action_log),
            exist_ok=True
        )


    def execute(
        self,
        actions,
        incident
    ):

        """
        Execute non-visual agent actions.

        Physical evidence capture is returned as a
        requested action and is executed by main.py,
        because main.py owns the current OpenCV frame.
        """

        results = []


        for action in actions:

            if action == "LOG_EVENT":

                results.append(
                    self._log_action(
                        action,
                        incident
                    )
                )


            elif action == "CAPTURE_EVIDENCE":

                results.append({
                    "action": action,
                    "status": "REQUESTED",
                    "message":
                        "Evidence capture requested by agent."
                })


            elif action == "GENERATE_ALERT":

                results.append(
                    self._generate_alert(
                        incident
                    )
                )


            elif action == "CONTINUE_MONITORING":

                results.append({
                    "action": action,
                    "status": "ACTIVE",
                    "message":
                        "Continuous monitoring enabled."
                })


            elif action == "ESCALATE":

                results.append(
                    self._escalate(
                        incident
                    )
                )


            else:

                results.append({
                    "action": action,
                    "status": "UNKNOWN"
                })


        return results


    def _generate_alert(self, incident):

        message = (
            f"ALERT: "
            f"{incident['incident_type']} | "
            f"Risk {incident['risk_score']}/100 | "
            f"{incident['severity']}"
        )


        print()
        print("🚨 AGENT ALERT")
        print(message)
        print()


        return {
            "action": "GENERATE_ALERT",
            "status": "EXECUTED",
            "message": message
        }


    def _escalate(self, incident):

        message = (
            f"ESCALATION REQUIRED: "
            f"{incident['incident_type']} "
            f"({incident['severity']})"
        )


        print()
        print("⚠️ AGENT ESCALATION")
        print(message)
        print()


        return {
            "action": "ESCALATE",
            "status": "EXECUTED",
            "message": message
        }


    def _log_action(
        self,
        action,
        incident
    ):

        record = {

            "timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "action":
                action,

            "incident_id":
                incident.get(
                    "incident_id"
                ),

            "incident_type":
                incident.get(
                    "incident_type"
                ),

            "severity":
                incident.get(
                    "severity"
                ),

            "risk_score":
                incident.get(
                    "risk_score"
                )
        }


        records = []


        if os.path.exists(
            self.action_log
        ):

            try:

                with open(
                    self.action_log,
                    "r"
                ) as file:

                    records = json.load(file)

            except (
                json.JSONDecodeError,
                FileNotFoundError
            ):

                records = []


        records.append(
            record
        )


        with open(
            self.action_log,
            "w"
        ) as file:

            json.dump(
                records,
                file,
                indent=4
            )


        return {
            "action": action,
            "status": "EXECUTED",
            "message":
                "Agent action logged."
        }