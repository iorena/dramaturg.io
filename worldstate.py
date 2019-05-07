from character import Character
from location import Location

import random

class WorldState:
    def __init__(self):
        self.locations = [Location(), Location()]
        self.characters = [Character(self.getRandomLoc()), Character(self.getRandomLoc())]
        self.initializePossibleTransitions()

    def getRandomLoc(self):
        return random.choices(self.locations)[0]

    def __str__(self):
        return "Locations: " + ", ".join(map(str, self.locations)) + "\nCharacters: " + ", ".join(map(str, self.characters))

    def initializePossibleTransitions(self):
        """
        Creates a list of tuples representing all possible transitions, keeping the transition at random
        """
        transitionSpace = []
        for loc in self.locations:
            for loc2 in self.locations:
                if loc != loc2:
                    if random.random() > 0.5:
                        transitionSpace.append((loc, loc2))
        self.possibleTransitions = transitionSpace

    def getPossibleTransitions(self):
        print("Possible transitions:")
        for transition in self.possibleTransitions:
            print(str(transition[0]), "->", str(transition[1]))
