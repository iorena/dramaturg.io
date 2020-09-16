import argparse, random

from story.story import Story
from language.embeddings import Embeddings
from concepts.affect.mood import Mood
from concepts.affect.emotion import Emotion
from graph import draw_graph



def main(print_dev_data, personality, latex, graph, content, types, noprint):
    personalities = [{"O": random.random(), "C": random.random(), "E": random.random(), "A": random.random(), "N": random.uniform(-1, 0)}, None]
    relationships = [Mood(Emotion(None, None, None, -0.5)), None]
    if personality:
        ready = False
        while not ready:
            personality = input("Give 1st personality parameters (O C E A N)").split(" ")
            if len(personality) != 5:
                personality1 = None
                print("invalid option, using random personality")
            else:
                personality1 = {"O": float(personality[0]), "C": float(personality[1]), "E": float(personality[2]), "A": float(personality[3]), "N": float(personality[4])}
            personality = input("Give 2nd personality parameters (O C E A N)").split(" ")
            if len(personality) != 5:
                personality2 = None
                print("invalid option, using random personality")
            else:
                personality2 = {"O": float(personality[0]), "C": float(personality[1]), "E": float(personality[2]), "A": float(personality[3]), "N": float(personality[4])}
            is_ready = input(f"default moods are {Mood(personality1)} and {Mood(personality2)}, is this ok? (y/n)")
            if is_ready != "n":
                ready = True

        personalities = [personality1, personality2]

        relationship = input("Give relationship a->b parameters (P A D)").split(" ")
        if len(relationship) != 3:
            relationship1 = None
            print("invalid option, using random relationship")
        else:
            relationship1 = Mood(Emotion(None, float(relationship[0]), float(relationship[1]), float(relationship[2])))
        relationship = input("Give relationship b->a parameters (P A D)").split(" ")
        if len(relationship) != 3:
            relationship2 = None
            print("invalid option, using random relationship")
        else:
            relationship2 = Mood(Emotion(None, float(relationship[0]), float(relationship[1]), float(relationship[2])))

        relationships = [relationship1, relationship2]

    if content:
        character = input("Give third character")
        character_verb = input("Give verb related to character")
        inheritance_object = input("Give object")
        object_verb = input("Give verb related to object")

        embeddings = Embeddings(character, inheritance_object)
        story = Story(embeddings, personalities, relationships, character_verb, object_verb)
    else:
        embeddings = Embeddings("isoäiti", "museo")
        story = Story(embeddings, personalities, relationships, "kuolla", "ottaa")

    if graph:
        draw_graph(story)

    elif (print_dev_data or types) and not noprint:
        print(story)
        for i, situation in enumerate(story.situations):
            print(f"Tilanne {i+1}: | {story.situation_names[i]}\n")
            for j, sequence in enumerate(situation.sequences):
                print(f"Sequence{j}\n{sequence}\n\n")
    elif latex and not noprint:
        for i, situation in enumerate(story.situations):
            print(f" Scene {i + 1} & & \\\\\n")
            for j, sequence in enumerate(situation.sequences):
                print(f"{sequence.get_latex()}\n")
    elif not noprint:
        for char in story.world_state.characters:
            keywords = ', '.join(list(filter(lambda x: x is not None, [char.mood.get_character_description('pleasure'), char.mood.get_character_description('arousal'), char.mood.get_character_description('dominance')])))
            print(f"{char.name}: {keywords}")

        title = story.get_title()

        print(f"\n\n{title[0].upper() + title[1:]}\n")

        for i, situation in enumerate(story.situations):
            print(f"\nTilanne {i+1}\n")
            turns = []
            for seq in situation.sequences:
                for turn in seq.turns:
                    turns.append(turn)
            first = situation.speakers[0].name
            second = situation.speakers[1].name
            if any(situation.mood_change) and situation is not story.situations[-1]:
                mood_changes = []
                if first in situation.mood_change:
                    mood_changes.append(f"{first} {situation.mood_change[first]}")
                if second in situation.mood_change:
                    mood_changes.append(f"{second} {situation.mood_change[second]}")
                turns.append("(" + ", ".join(mood_changes) + ")")

            uppercased = turns[0].inflected[0].upper()
            line = uppercased + turns[0].inflected[1:]
            if line [-1] == "?":
                line = line[0:-2] + line[-1]
            line += ". " if line[-1] != "?" else " "
            last_turn = turns[0]
            for turn in turns:
                if turn is None:
                    continue
                if len(turn.inflected) < 1:
                    continue
                line = ""
                uppercased = turn.inflected[0].upper()
                line += uppercased + turn.inflected[1:]
                if line [-1] == "?":
                    line = line[0:-2] + line[-1]
                line += ". " if line[-1] != "?" else " "
                sentence_type = turn.get_sentence_type()
                if types:
                    print(f"\t{turn.speaker.name}  {sentence_type}\n{line}")
                else:
                    print(f"\t{turn.speaker.name}\n{line}")




def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("someargument", nargs="?", default=None)
    parser.add_argument("-d", "--development", help="Show action type names and mood", action='store_true')
    parser.add_argument("-p", "--personality", help="Set personality parameters", action='store_true')
    parser.add_argument("-l", "--latex", help="Set personality parameters", action='store_true')
    parser.add_argument("-g", "--graph", help="Draw graph", action='store_true')
    parser.add_argument("-c", "--content", help="Choose content", action='store_true')
    parser.add_argument("-t", "--types", help="Print human-friendly names of sentence types", action="store_true")
    parser.add_argument("-n", "--noprint", help="Don't print story, just debug log", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(args)
    main(args.development, args.personality, args.latex, args.graph, args.content, args.types, args.noprint)
