import csv

def load_pad_values(action_types, path="../data/action_types_to_pad.csv"):
    padded_action_types = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="\t")
        for row in csv_reader:
            action_type = action_types[row[0]]
            padded_action_types.append(action_type.add_pad_data(float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]), float(row[9])))
    print("added action types")
    return padded_action_types
