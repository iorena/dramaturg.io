import random


class WorldObject:
    id_counter = 0

    def __init__(self, name, id=None):
        if id is None:
            self.id = WorldObject.id_counter
            WorldObject.id_counter += 1
        else:
            self.id = id
        self.attributes = {}
        if self.id in range(90, 95):
            self.attributes["appraisal"] = self
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if type(other) is str:
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self)

    def set_owner(self, owner):
        self.attributes["owner"] = owner

    def set_location(self, location):
        self.attributes["location"] = location
