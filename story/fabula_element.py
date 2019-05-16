from concepts import location


class FabulaElement:
    def __init__(self, elem, subj, world_state):
        self.elem = elem
        self.subj = subj
        self.world_state = world_state
        self.obj = self.get_object()
        self.transition = self.get_transition()

    def __str(self):
        return self.elem

    def get_object(self):
        """
        Todo: replace hard-coding with actual functionality
        """
        if self.elem is "G":
            return self.subj
        if self.elem is "A":
            return self.subj
        if self.elem is "P":
            return None
        if self.elem is "IE":
            return None

    def get_transition(self):
        """
        Todo: Ditto
        """
        if self.elem is "G":
            return {"location": location.Location(0)}
        if self.elem is "A":
            return {"location": location.Location(0)}
        if self.elem is "P":
            return {"location": location.Location(0)}
        if self.elem is "IE":
            return {"affect": "sadness"}
