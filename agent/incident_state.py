from datetime import datetime


class IncidentState:

    def __init__(self):
        self.active = False

        self.incident_id = None
        self.incident_type = None

        self.first_seen = None
        self.last_seen = None

        self.detection_count = 0

        self.fire_seen = False
        self.smoke_seen = False
        self.person_seen = False
        self.fall_seen = False
        self.restricted_seen = False

        self.person_at_risk = False

        self.risk_score = 0
        self.severity = "LOW"

        self.status = "NORMAL"

        self.actions = []

    def start_incident(
        self,
        incident_id,
        incident_type
    ):

        self.active = True

        self.incident_id = incident_id

        self.incident_type = incident_type

        self.first_seen = datetime.now()

        self.last_seen = self.first_seen

        self.status = "ACTIVE"

    def update(self):

        self.last_seen = datetime.now()

        self.detection_count += 1

    def reset(self):

        self.__init__()