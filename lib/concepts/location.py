from concepts.worldobject import WorldObject

import random

APPRAISALS = ["horrible", "bad", "okay", "good", "great"]


class Location:
    id_counter = 0
    names = ["talo", "mökki", "katu", "luola"]
    #appraisals from 0 = horrible to 4 = great
    appraisals = [2, 3, 1, 2]

    def __init__(self, id=None):
        if id is None:
            self.id = Location.id_counter
            Location.id_counter += 1
        else:
            self.id = id
        score = Location.appraisals[self.id]
        self.attributes = {"appraisal": WorldObject(90 + score, APPRAISALS[score])}
        location_type = random.choices(Location.names)[0]
        Location.names.remove(location_type)
        self.name = location_type

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.name)
