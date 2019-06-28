import csv


def load_expansion_types(path="../data/expansion_types.csv"):
    expansions = {}
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            expansions[row[0]] = {"pre_expansions": row[1].split(", "), "infix_expansions": row[2].split(", "),
                                  "post_expansions": row[3].split(", ")}
    return expansions
