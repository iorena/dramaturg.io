import argparse

from concepts.character import Character
from concepts.world import World


def main(world):
    w = World(world)
    print(w.name)
    c1 = Character("Pekka")
    c2 = Character("Ritva")

    print(c1.greet())
    print(c2.greet())


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--world", help="Name of world to create.", default="Uusi Maa")
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    main(**arguments())
