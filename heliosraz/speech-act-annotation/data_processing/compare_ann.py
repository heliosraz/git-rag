import json
from collections import defaultdict
import os


def load_annotations_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    annotations = []
    for entry in data:
        for annotation in entry["annotations"]:
            span_labels = {}
            for item in annotation["result"]:
                span_text = item["value"]["text"]  # Extract the text of the span
                if span_text not in span_labels:
                    span_labels[span_text] = []
                # Skip 'Turn' label and add other labels
                if "labels" in item["value"] and item["value"]["labels"][0] == "Turn":
                    continue
                if "choices" in item["value"]:
                    span_labels[span_text].extend(item["value"]["choices"])
            # Now add each span with its labels to the annotations list
            for text, labels in span_labels.items():
                start = item["value"]["start"]
                end = item["value"]["end"]
                annotations.append((text, (start, end), labels))
    return annotations


def compare_annotations(annotations_list):
    agreements = defaultdict(list)
    disagreements = defaultdict(list)

    # Helper function to prepare labels for comparison by removing 'Turn' and sorting
    def prepare_labels(labels):
        filtered_labels = [label for label in labels if label != "Turn"]
        return set(filtered_labels)

    # Iterate over all annotations using index to avoid comparing the same pairs multiple times
    for i, annotations_i in enumerate(annotations_list):
        for j in range(
            i + 1, len(annotations_list)
        ):  # Compare only with following annotators
            annotations_j = annotations_list[j]
            for text_i, span_i, labels_i in annotations_i:
                for text_j, span_j, labels_j in annotations_j:
                    if (
                        text_i == text_j and span_i == span_j
                    ):  # Compare based on the span text and indices
                        prepared_labels_i = prepare_labels(labels_i)
                        prepared_labels_j = prepare_labels(labels_j)
                        if prepared_labels_i == prepared_labels_j:
                            agreements[(i, j)].append((text_i, span_i, labels_i))
                        else:
                            disagreements[(i, j)].append(
                                (text_i, span_i, labels_i, labels_j)
                            )

    return agreements, disagreements


if __name__ == "__main__":
    # Example usage
    annotations_folder = "../annotations"
    file_paths = [
        load_annotations_from_json(os.path.join(root, file))
        for root, dirs, files in os.walk(annotations_folder)
        for file in files
    ]

    agreements, disagreements = compare_annotations(file_paths)

    print("Agreements:")
    if not agreements:  # Check if there are any agreements to print
        print("No agreements found.")
    else:
        for (annotator1, annotator2), spans in agreements.items():
            print(
                f"Annotations between annotator {annotator1 + 1} and annotator {annotator2 + 1} agree on:"
            )
            for text, span_indices, labels in spans:
                print(f'  Span: "{text}" ({span_indices[0]}, {span_indices[1]})')
                print(f"  Labels: {', '.join(labels)}")

    print("\nDisagreements:")
    if not disagreements:  # Check if there are any disagreements to print
        print("No disagreements found.")
    else:
        for (annotator1, annotator2), spans in disagreements.items():
            print(
                f"Annotations between annotator {annotator1 + 1} and annotator {annotator2 + 1} disagree on:"
            )
            for text, span_indices, labels1, labels2 in spans:
                print(f'  Span: "{text}" ({span_indices[0]}, {span_indices[1]})')
                print(f"  Labels 1: {', '.join(labels1)}")
                print(f"  Labels 2: {', '.join(labels2)}")
