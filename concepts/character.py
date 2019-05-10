from language.style import Style
import random

NAMES = ["Pekka", "Ville", "Kalle", "Maija"]


class Character:
    id_counter = 0

    def __init__(self, location):
        self.id = Character.id_counter
        Character.id_counter += 1
        self.attributes = {"location": location}
        self.goals = []
        self.name = self.random_name()
        self.perception = None
        self.style = Style(random.random(), random.random())

    def __str__(self):
        return (f"{{Character{str(self.id)} location: {self.attributes['location']} goal: "
                f"{self.goals[0].characters[0].attributes['location']}}}")

    def random_name(self):
        return random.choices(NAMES)[0]

    def set_perception(self, world_state):
        self.perception = world_state

    def set_goal(self, goal):
        self.goals.append(goal)
