import argparse

from story.story import Story


def main(do_story):
    if do_story:
        story = Story()
        print(story)
    else:
        print("Did nothing!")


def parse_arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("someargument", nargs="?", default=None)
    parser.add_argument("-s", "--story", help="Create a story!", action='store_true')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print(args)
    main(args.story)
