import argparse

from story.story import Story
from language.embeddings import Embeddings


def main(do_story, print_dev_data):
    if do_story and print_dev_data:
        embeddings = Embeddings()
        story = Story(embeddings)
        print(story)
        for i, situation in enumerate(story.situations):
            print(f"Situation{i}: {situation.location}\n")
            for j, sequence in enumerate(situation.sequences):
                print(f"Sequence{j}\n{sequence}\n\n")
    elif do_story:
        embeddings = Embeddings()
        story = Story(embeddings)
        for char in story.world_state.characters:
            keywords = ', '.join(list(filter(lambda x: x is not None, [char.mood.get_character_description('pleasure'), char.mood.get_character_description('arousal'), char.mood.get_character_description('dominance')])))
            print(f"{char.name}: {keywords}")

        title = story.get_title()

        print(f"\n\n{title[0].upper() + title[1:]}\n")

        for i, situation in enumerate(story.situations):
            print(f"\nKohtaus {i+1}: {situation.location}\n")
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
            for turn in turns[1:]:
                line = ""
                uppercased = turn.inflected[0].upper()
                line += uppercased + turn.inflected[1:]
                if line [-1] == "?":
                    line = line[0:-2] + line[-1]
                line += ". " if line[-1] != "?" else " "
                print(f"\t{turn.speaker.name}\n{line}")
    else:
        print("Did nothing!")


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("someargument", nargs="?", default=None)
    parser.add_argument("-s", "--story", help="Create a story!", action='store_true')
    parser.add_argument("-d", "--development", help="Show action type names and mood", action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(args)
    main(args.story, args.development)
