from uuid import uuid4

from agent.incident_state import IncidentState
from agent.incident_memory import IncidentMemory
from agent.response_policy import get_response_policy
from agent.action_executor import ActionExecutor


class IncidentAgent:

    def __init__(self):

        self.state = IncidentState()
        self.memory = IncidentMemory()
        self.action_executor = ActionExecutor()


    # PROCESS CONFIRMED EVENT

    def process_event(self, event):

        self._update_state(event)

        incident_type = self._determine_incident_type()


        # Start a new incident
        if not self.state.active:

            self.state.start_incident(
                incident_id=(
                    f"INC-{uuid4().hex[:8].upper()}"
                ),
                incident_type=incident_type
            )


        self.state.update()


        # Calculate contextual risk
        risk_score = self._calculate_risk()

        severity = self._get_severity(
            risk_score
        )


        self.state.incident_type = incident_type
        self.state.risk_score = risk_score
        self.state.severity = severity


        policy = get_response_policy(
            severity
        )


        self.state.actions = policy["actions"]

        # Execute the actions selected by the agent
        action_results = self.action_executor.execute(
            policy["actions"],
            {
                "incident_id": self.state.incident_id,
                "incident_type": incident_type,
                "risk_score": risk_score,
                "severity": severity
            }
        )


        return {
            "incident_id": self.state.incident_id,
            "incident_type": incident_type,
            "risk_score": risk_score,
            "severity": severity,
            "status": self.state.status,

            "actions": policy["actions"],

            "action_results": action_results,

            "message": policy["message"],

            "factors": self._get_risk_factors()
        }


    # UPDATE STATE

    def _update_state(self, event):

        self.state.fire_seen |= bool(
            event.get("fire", False)
        )

        self.state.smoke_seen |= bool(
            event.get("smoke", False)
        )

        self.state.person_seen |= bool(
            event.get("person", False)
        )

        self.state.fall_seen |= bool(
            event.get("fall", False)
        )

        self.state.restricted_seen |= bool(
            event.get("restricted", False)
        )

        self.state.person_at_risk |= bool(
            event.get("person_at_risk", False)
        )


    # CONTEXTUAL RISK ENGINE

    def _calculate_risk(self):

        score = 0


        # ----------------------------------------------------
        # FIRE
        # ----------------------------------------------------

        if self.state.fire_seen:

            score += 50


        # ----------------------------------------------------
        # SMOKE
        # ----------------------------------------------------

        if self.state.smoke_seen:

            score += 20


        # ----------------------------------------------------
        # FALL
        # ----------------------------------------------------

        if self.state.fall_seen:

            score += 45


        # ----------------------------------------------------
        # RESTRICTED AREA
        # ----------------------------------------------------

        if self.state.restricted_seen:

            score += 25


        # ----------------------------------------------------
        # PERSON PRESENT
        # ----------------------------------------------------

        if self.state.person_seen:

            score += 5


        # ----------------------------------------------------
        # PERSON EXPOSED TO HAZARD
        # ----------------------------------------------------

        if self.state.person_at_risk:

            score += 30


        return min(score, 100)


    # SEVERITY

    def _get_severity(self, score):

        if score >= 80:
            return "CRITICAL"

        if score >= 50:
            return "HIGH"

        if score >= 25:
            return "MEDIUM"

        return "LOW"


    # INCIDENT TYPE

    def _determine_incident_type(self):

        if (
            self.state.fire_seen
            and self.state.person_at_risk
        ):
            return "FIRE_WITH_HUMAN_EXPOSURE"


        if self.state.fire_seen:
            return "FIRE"


        if self.state.fall_seen:
            return "POSSIBLE_FALL"


        if self.state.restricted_seen:
            return "RESTRICTED_AREA_ENTRY"


        if self.state.smoke_seen:
            return "SMOKE_DETECTED"


        return "UNKNOWN_EVENT"


    # RISK FACTORS

    def _get_risk_factors(self):

        factors = []


        if self.state.fire_seen:
            factors.append("fire_detected")


        if self.state.smoke_seen:
            factors.append("smoke_detected")


        if self.state.person_seen:
            factors.append("person_detected")


        if self.state.fall_seen:
            factors.append("possible_fall")


        if self.state.restricted_seen:
            factors.append(
                "restricted_area_entry"
            )


        if self.state.person_at_risk:
            factors.append(
                "person_at_risk"
            )


        return factors


    # RESOLVE INCIDENT

    def resolve_incident(self):

        if not self.state.active:
            return


        self.memory.add({

            "incident_id":
                self.state.incident_id,

            "incident_type":
                self.state.incident_type,

            "severity":
                self.state.severity,

            "risk_score":
                self.state.risk_score,

            "detection_count":
                self.state.detection_count
        })


        self.state.reset()