import argparse, random
from bs4 import BeautifulSoup

from story.story import Story
from utils.textparser import TextParser
from language.embeddings import Embeddings
from concepts.affect.mood import Mood
from concepts.affect.emotion import Emotion



def main(input_file, print_dev_data, personality, latex, graph, content, types, noprint, text_input):
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
        pre_subject = input("Give preproject subject ")
        pre_verb = input("Give preproject verb ")
        pre_object = input("Give preproject object ")
        main_subject = input("Give main project subject ")
        main_verb = input("Give main project verb ")
        main_object = input("Give main project object ")
        counter_subject = input("Give counterproject subject ")
        counter_verb = input("Give counterproject verb ")
        counter_object = input("Give counterproject object ")

        # embeddings disaled for now, edit to add randomness
        embeddings = Embeddings([pre_subject, main_subject, counter_subject], [pre_object, main_object, counter_object], False)
        story = Story(embeddings, personalities, relationships, [pre_verb, main_verb, counter_verb])
    elif text_input:
        lines = None
        with open(input_file) as f:
            lines = ''.join(f.readlines())
            f.close()

        soup = BeautifulSoup(lines, 'html.parser')

        parags = []
        for paragraph in soup.find_all('p', class_='yle__article__paragraph'):
            parags.append(paragraph.text)

        text = ''.join(parags)
        parser = TextParser()
        parser.parse_bow(text)
        subjects, verbs, objects = parser.get_play_words()

        embeddings = Embeddings(subjects, objects, False)
        story = Story(embeddings, personalities, relationships, verbs)
    else:
        embeddings = Embeddings(["kirkko", "museo", "museo"], ["valmis", "rakennettava", "kallis"], False)
        story = Story(embeddings, personalities, relationships, ["olla", "olla", "olla"])


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
            print(f" Situation {i + 1} & & \\\\\n")
            for j, sequence in enumerate(situation.sequences):
                print(f"{sequence.get_latex()}\n")
    elif not noprint:
        for char in story.world_state.characters:
            keywords = ', '.join(list(filter(lambda x: x is not None, [char.mood.get_character_description('pleasure'), char.mood.get_character_description('arousal'), char.mood.get_character_description('dominance')])))
            print(f"{char.name}: {keywords}")

        title = "Kuunnelma 1" #let's not use embeddings now. // story.get_title()

        print(f"\n\n{title[0].upper() + title[1:]}\n")

        for i, situation in enumerate(story.situations):
            print(f"\nTilanne {i+1}\n")
            turns = []
            for seq in situation.sequences:
                for turn in seq.turns:
                    uppercased = turn.inflected[0].upper()
                    line = uppercased + turn.inflected[1:]
                    if line [-1] == "?":
                        line = line[0:-2] + line[-1]
                    line += ". " if line[-1] != "?" else " "
                    sentence_type = turn.get_sentence_type()
                    if types:
                        turns.append(f"\t{turn.speaker.name}  {sentence_type}\n{line}")
                    else:
                        turns.append(f"\t{turn.speaker.name}\n{line}")

                    if any(turn.verbalized_change):
                        mood_changes = []
                        first = situation.speakers[0].name
                        second = situation.speakers[1].name
                        if first in turn.verbalized_change:
                            mood_changes.append(f"{first} {turn.verbalized_change[first]}")
                        if second in turn.verbalized_change:
                            mood_changes.append(f"{second} {turn.verbalized_change[second]}")
                        turns.append("(" + ", ".join(mood_changes) + ")")

            for turn in turns:
                print(turn)





def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("input_file", nargs="?", default=None)
    parser.add_argument("-d", "--development", help="Show action type names and mood", action='store_true')
    parser.add_argument("-p", "--personality", help="Set personality parameters", action='store_true')
    parser.add_argument("-l", "--latex", help="Set personality parameters", action='store_true')
    parser.add_argument("-g", "--graph", help="Draw graph", action='store_true')
    parser.add_argument("-c", "--content", help="Choose content", action='store_true')
    parser.add_argument("-t", "--types", help="Print human-friendly names of sentence types", action="store_true")
    parser.add_argument("-n", "--noprint", help="Don't print story, just debug log", action="store_true")
    parser.add_argument("-i", "--text_input", help="Read txt file to pick words from", action="store_true")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(args)
    main(args.input_file, args.development, args.personality, args.latex, args.graph, args.content, args.types, args.noprint, args.text_input)
