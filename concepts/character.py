
class Character:
    id_counter = 0

    def __init__(self, location):
        self.id = Character.id_counter
        Character.id_counter += 1
        self.attributes = {"location": location}
        self.goals = []
        self.perception = None

    def __str__(self):
        return (f"{{Character{str(self.id)} location: {self.attributes['location']} goal: "
                f"{self.goals[0].characters[0].attributes['location']}}}")

    def set_perception(self, world_state):
        self.perception = world_state

    def set_goal(self, goal):
        self.goals.append(goal)
