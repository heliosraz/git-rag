import pandas as pd
import os
from collections import Counter, defaultdict


def kappa(data: pd.DataFrame):
    for i, row in data.iterrows():
        for annotations in zip(row.iloc[1:]):
            print([type(item) for item in [l for l in annotations]])
            flattened = [
                annotation["value"]
                for annotation in [item["result"] for item in [l for l in annotations]]
            ]
            print(flattened[0])
            # tag_counts=Counter(flattened)
            # print(tag_counts)


def compile_data(file):
    result = pd.DataFrame(columns=["data", "annotations"])
    annotations = []
    df = pd.read_json(file, encoding="utf-8")
    df["data"] = [r["text"] for r in df["data"]]
    for j, row in enumerate(df["annotations"]):
        annotation_dict = defaultdict(set)
        for annotation in row[0]["result"]:
            if "choices" in annotation["value"]:
                annotation_dict[annotation["value"]["text"]].add(
                    annotation["value"]["choices"][0]
                )
        annotations.append(dict(annotation_dict))
    df.loc[:, "annotations"] = annotations
    return df


if __name__ == "__main__":
    annotations_folder = "../annotations"
    file_paths = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(annotations_folder)
        for file in files
    ]
    data = pd.DataFrame(columns=["data"])
    for i, file in enumerate(file_paths):
        annotations = compile_data(file)
        annotations = annotations.rename(columns={"annotations": f"annotations_{i}"})
        # initializing data column
        if len(data["data"]) < 1:
            data["data"] = annotations["data"]
        # merging new data
        data = pd.merge(
            data,
            annotations.loc[:, [f"data", f"annotations_{i}"]],
            on="data",
            how="left",
        )
    # catch nan entries
    data = data.applymap(lambda x: {} if pd.isnull(x) else x)
