import os
import re
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from typing import List

special_char = ["\\", ".", "+", "*", "?", "^", "$", "(", ")", "[", "]", "{", "}", "|"]


def preprocess(file: str):
    document = ""
    print(file)
    with open(file, "r", encoding="utf-8") as f:
        file_string = f.read().strip()


def preannotation(root: str):
    document_sentences_dict = {}
    result = []
    for root, dirs, files in os.walk(root):
        # formatting
        # {"data": {"text": "Close"}, "predictions": [{"model_version": "one", "result": [
        #     {"value": {"start": 0, "end": 5, "text": "Close", "labels": ["Turn"]}, "from_name": "Turn",
        #      "to_name": "text", "type": "labels"}]}]}
        for file in files:
            if not file == ".DS_Store":
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    for line in f:
                        print("test")
                        print(sent_tokenize(line))
        with open(
            "../data/processed_" + root.split("/")[-1] + ".json", "a", encoding="utf-8"
        ) as f:
            print(json.dumps(result), file=f)


if __name__ == "__main__":
    data_folder = "../data/raw_data"
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            print(os.path.join(root, file))
            if not file == ".DS_Store":
                preprocess(os.path.join(root, file))
    for root, dirs, files in os.walk(data_folder):
        if files:
            preannotation(root)
    # preannotation()
