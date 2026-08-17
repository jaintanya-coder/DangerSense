from collections import deque
from datetime import datetime


class IncidentMemory:

    def __init__(self, max_incidents=20):

        self.incidents = deque(
            maxlen=max_incidents
        )


    def add(self, incident):

        self.incidents.append({
            "timestamp": datetime.now().isoformat(),
            **incident
        })


    def get_recent(self, limit=5):

        return list(
            self.incidents
        )[-limit:]


    def count_recent(
        self,
        incident_type
    ):

        return sum(
            1
            for incident in self.incidents
            if incident.get(
                "incident_type"
            ) == incident_type
        )


    def clear(self):

        self.incidents.clear()