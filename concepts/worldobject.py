
import random


class WorldObject:
    id_counter = 0
    names = ["koiranpentu", "jäätelö", "makkara"]

    def __init__(self, id=None):
        if id is None:
            self.id = WorldObject.id_counter
            WorldObject.id_counter += 1
        else:
            self.id = id
        self.attributes = {}
        object_type = random.choices(WorldObject.names)[0]
        WorldObject.names.remove(object_type)
        self.attributes["type"] = object_type

    def __str__(self):
        return self.attributes["type"]

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.attributes["type"])

    def set_owner(self, owner):
        self.attributes["owner"] = owner

    def set_location(self, location):
        self.attributes["location"] = location
