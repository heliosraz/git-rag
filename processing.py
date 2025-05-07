import json
import os
import pandas as pd
from tqdm import tqdm
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)

def format_chunk(document, chunk_num, file_type, content, project, path):
    return {
        "document_name": document,
        "chunk_id": "{num:0{width}}".format(num=chunk_num, width=5),
        "content": content,
        "project_name": project,
        "address": path,
        "type": file_type,
        "doc_chunks": [],
        "project_chunks": []
    }


def save_result(doc_chunks: dict, project_name: str):
    doc = fix_doc_chunks(doc_chunks)
    result = join_project_chunks(project_name, doc)
    with open(f"./data/{project_name}.json", "w") as file:
        json.dump(list(result.values()), file, indent=4)


def fix_project_chunks(project: dict):
    for chunk in project:
        project[chunk]["project_chunks"] = list(project.keys())
    return project


def fix_doc_chunks(doc: dict):
    for chunk in doc:
        doc[chunk]["doc_chunks"] = list(doc.keys())
    return doc


def join_project_chunks(project_name: str, chunks: dict):
    result = {}
    if os.path.exists(f"./data/{project_name}.json"):
        with open(f"./data/{project_name}.json", "r") as json_file:
            result = {row["chunk_id"]: row for row in json.load(json_file)}
            result.update(chunks)
    if not result:
        result = chunks
    result = fix_project_chunks(result)
    return result

def process_code(splitter, project_name, file_path, chunk_id, file_type):
    document = file_path.split("/")[-1]
    doc = {}
    with open(file_path, "r") as file:
        content = file.read()
        chunks = splitter.split_text(content)
        for chunk in chunks:
            doc["chunk_" + "{num:0{width}}".format(num=chunk_id, width=5)] = (
                format_chunk(document, chunk_id, file_type, chunk, project_name, file_path)
            )
            chunk_id += 1
    save_result(doc, project_name) 
    return chunk_id

def main():

    save_data = "./data"
    ignore = {"data", "raw_data", "__pycache__", "annotations"}
    text_splitters = {
        "py": RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=300, chunk_overlap=300
    ),
        # "ipynb": process_ipynb,
        "js": RecursiveCharacterTextSplitter.from_language(
        language=Language.JS, chunk_size=150, chunk_overlap=150
    ),
        "html": RecursiveCharacterTextSplitter.from_language(
        language=Language.HTML, chunk_size=300, chunk_overlap=300
    ),
        "java": RecursiveCharacterTextSplitter.from_language(
        language=Language.JAVA, chunk_size=300, chunk_overlap=300
    ),
        "tex": RecursiveCharacterTextSplitter.from_language(
        language=Language.LATEX, chunk_size=150, chunk_overlap=150
    ),
        "Rmd": RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN, chunk_size=300, chunk_overlap=300
    ),
        "md": RecursiveCharacterTextSplitter.from_language(
        language=Language.MARKDOWN, chunk_size=300, chunk_overlap=300
    ),
    }
    chunk_id = 0

    for root, dirs, files in os.walk("./heliosraz"):
        print(root, len(files))
        print(f"Processing {root}")
        if len(root.split("/")) >= 3: 
            if len(root.split("/")) > 3:
                directory = root.split("/")[3]
            else:
                directory = ""
            project_name = root.split("/")[2]
            if directory in ignore:
                continue
            for f in tqdm(files):
                file_type = f.split(".")[-1]
                if file_type in text_splitters:
                    print(f"File: {f}")
                    chunk_id = process_code(text_splitters[file_type], project_name, os.path.join(root, f), chunk_id = chunk_id, file_type= file_type)

    for root, dirs, files in os.walk("./data"):
        for fp in files:
            print(fp, len(list(pd.read_json(os.path.join(root, fp)).iterrows())))

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(script_dir, "data"), exist_ok = True)
    main()