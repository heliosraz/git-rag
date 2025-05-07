import json
import csv
import nltk

# def count_unique_words(file_path):
#     unique_words = set()
#     with open(file_path, 'r', encoding='utf-8') as file:
#         for line in file:
#             words = line.split()
#             unique_words.update(words)
#     return len(unique_words)

speech_acts = []
clause_types = []


def preprocess_data(file_path, speech, clause):
    f = open(file_path)

    data = json.load(f)

    # print(data[0]["annotations"][0]["result"][0]["value"]["choices"])

    for document in data:
        for id in document["annotations"]:
            for v in id["result"]:
                if "choices" in v["value"]:
                    if (
                        len(v["value"]["choices"][0].split()) == 2
                        and v["value"]["choices"][0].split()[1] == "Clause"
                    ):
                        clause.append((v["value"]["text"], v["value"]["choices"]))
                    else:
                        speech.append((v["value"]["text"], v["value"]["choices"]))

    # print(clause)
    # print(speech)

    f.close()


preprocess_data(
    "data/project-2-at-2024-05-03-18-22-da5d8ca1.json", speech_acts, clause_types
)
preprocess_data(
    "data/project-5-at-2024-04-28-02-09-d9ec588d.json", speech_acts, clause_types
)
preprocess_data(
    "data/project-13-at-2024-05-05-17-51-ba15127f.json", speech_acts, clause_types
)
preprocess_data(
    "data/project-17-at-2024-05-05-16-17-d3c3de99.json", speech_acts, clause_types
)

# print(relations)

with open("all_speech_tags.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(("span", "label"))
    writer.writerows(speech_acts)

with open("all_clause_types.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(("span", "label"))
    writer.writerows(clause_types)
