import random


class Location:
    id_counter = 0

    def __init__(self, id=None):
        if id is None:
            self.id = Location.id_counter
            Location.id_counter += 1
        else:
            self.id = id
        self.keywords = self.getKeywords()

    def __str__(self):
        return "Location" + str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def getKeywords(self):
        location_type = random.choices(["talo", "mökki", "katu", "luola"])[0]
        return {"type": location_type}

