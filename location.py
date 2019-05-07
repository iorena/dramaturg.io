

class Location:
    id_counter = 0
    def __init__(self):
        self.id = Location.id_counter
        Location.id_counter += 1

    def __str__(self):
        return "Location" + str(self.id)

    def __eq__(self, other):
        return self.id == other.id
