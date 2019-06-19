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
        self.keywords = self.get_keywords()
        self.name = self.keywords["type"]

    def __str__(self):
        return self.keywords["type"]

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.keywords["type"])

    def get_keywords(self):
        location_type = random.choices(Location.names)[0]
        Location.names.remove(location_type)
        return {"type": location_type}

