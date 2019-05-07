
class Character:
    id_counter = 1

    def __init__(self, location):
        self.id = Character.id_counter
        Character.id_counter += 1
        self.attributes = {"location": location}

    def __str__(self):
        return "{Character" + str(self.id) + " location: " + str(self.attributes["location"]) + "}"
