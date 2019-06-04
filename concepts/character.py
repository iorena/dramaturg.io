from language.style import Style
import random



class Character:
    id_counter = 0
    names = ["Pekka", "Ville", "Kalle", "Maija"]

    def __init__(self, location):
        self.id = Character.id_counter
        Character.id_counter += 1
        self.attributes = {"location": location}
        self.goals = []
        self.name = self.random_name()
        self.perception = None
        self.relations = {}
        self.style = Style(random.random(), random.random())

    def __str__(self):
        return self.name
        """
        return (f"{{Character{str(self.id)} location: {self.attributes['location']} goal: "
                f"{self.goals[0].characters[0].attributes['location']}}}")
        """

    def __hash__(self):
        return hash(self.name)

    def random_name(self):
        name = random.choices(Character.names)[0]
        Character.names.remove(name)
        return name

    def set_perception(self, world_state):
        self.perception = world_state

    def set_goal(self, goal):
        self.goals.append(goal)

    def set_relation(self, other, relation):
        """
        After creating characters, set relations towards each character. For now, one-dimensional value between 0 and 1.
        Todo: factorize relationship into different aspects; closeness, appreciation...?
        """
        self.relations[other.name] = relation
