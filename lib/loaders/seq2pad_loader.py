import csv

def load_pad_values(path="../data/seq_and_action_types_to_pad.csv"):
    values = {}
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            values[row[0]] = (float(row[1]), float(row[2]), float(row[3]))
    return values


