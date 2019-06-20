import random


class Location:
    id_counter = 0
    names = ["talo", "mökki", "katu", "luola"]

    def __init__(self, id=None):
        if id is None:
            self.id = Location.id_counter
            Location.id_counter += 1
        else:
            self.id = id
        self.attributes = {}
        location_type = random.choices(Location.names)[0]
        Location.names.remove(location_type)
        self.name = location_type

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.name)
