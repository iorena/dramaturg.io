from concepts import location
from concepts.worldstate import WorldState


class FabulaElement:
    def __init__(self, elem, subj, world_state):
        self.elem = elem
        self.subj = subj
        self.world_state = world_state
        self.obj = self.getObject()
        self.transition = self.getTransition()

    def __str(self):
        return self.elem

    def getObject(self):
        if self.elem is "G":
            return self.subj
        if self.elem is "A":
            return self.subj
        if self.elem is "P":
            return None
        if self.elem is "IE":
            return None

    def getTransition(self):
        if self.elem is "G":
            return {"location": location.Location(0)}
        if self.elem is "A":
            return {"location": location.Location(0)}
        if self.elem is "P":
            return WorldState(self.world_state)
        if self.elem is "IE":
            return {"affect": "sadness"}
