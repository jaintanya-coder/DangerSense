class EventTracker:
    """
    Tracks safety events across consecutive frames.

    An event must remain present for a specified number
    of consecutive frames before it becomes confirmed.

    A confirmed event is logged only once until the
    incident disappears.
    """

    def __init__(self, required_frames=8):

        self.required_frames = required_frames

        # Number of consecutive frames for each event
        self.counters = {}

        # Currently confirmed incidents
        self.active_events = set()


    def update(self, event_name, detected):
        """
        Update the tracker for the current frame.

        Returns:
            True only when an event is confirmed.
        """

        # No event detected

        if not detected:

            self.counters[event_name] = 0

            self.active_events.discard(
                event_name
            )

            return False

        # Event detected

        current_count = self.counters.get(
            event_name,
            0
        )

        current_count += 1

        self.counters[event_name] = current_count


        # Already confirmed

        if event_name in self.active_events:

            return False


        # Confirm new incident
        if current_count >= self.required_frames:

            self.active_events.add(
                event_name
            )

            return True


        return False


    def reset_all(self):
        """
        Reset all active incidents.
        """

        self.counters.clear()

        self.active_events.clear()