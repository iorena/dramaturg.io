from concepts.worldobject import WorldObject

import random

APPRAISALS = ["horrible", "bad", "okay", "good", "great"]
WEATHERS = ["sunny", "cloudy", "rainy", "stormy"]


class Location:
    id_counter = 0
    names = ["koti", "mökki"]
    #appraisals from 0 = horrible to 4 = great
    appraisals = [2, 3, 1, 2]

    def __init__(self, id=None):
        if id is None:
            self.id = Location.id_counter
            Location.id_counter += 1
        else:
            self.id = id
        score = Location.appraisals[self.id]
        weather_score = random.randint(0, 3)
        self.attributes = {"appraisal": WorldObject(APPRAISALS[score], 90 + score), "weather": WorldObject(WEATHERS[weather_score], 95 + weather_score)}
        location_type = Location.names[self.id]
        self.name = location_type

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.name)
