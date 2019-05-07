
class Character:
    id_counter = 0

    def __init__(self, location):
        self.id = Character.id_counter
        Character.id_counter += 1
        self.attributes = {"location": location}
        self.goals = []

    def __str__(self):
        return "{Character" + str(self.id) + " location: " + str(self.attributes["location"]) + " goal: " + str(self.goals[0].characters[0].attributes["location"]) + "}"

    def setPerception(self, worldState):
        self.perception = worldState

    def setGoal(self, goal):
        self.goals.append(goal)
