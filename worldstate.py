from character import Character
from location import Location

import random

class WorldState:
    def __init__(self, old=None):
        if old == None:
            self.initializeStoryWorld()
        else:
            self.locations = old.locations
            self.characters = old.characters

    def initializeStoryWorld(self):
        self.locations = [Location(), Location()]
        self.characters = [Character(self.getRandomLoc()), Character(self.getRandomLoc())]

    def getRandomLoc(self):
        return random.choices(self.locations)[0]

    def __str__(self):
        return "Locations: " + ", ".join(map(str, self.locations)) + "\nCharacters: " + ", ".join(map(str, self.characters))

    def __eq__(self, other):
        if other is None:
            return False
        for i in range(len(self.locations)):
            if other.locations[i] != self.locations[i]:
                return False
        for i in range(len(self.characters)):
            if other.characters[i].attributes != self.characters[i].attributes:
                return False
        return True
