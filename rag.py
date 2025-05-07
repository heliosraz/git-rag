import os
script_dir = os.path.dirname(os.path.abspath(__file__))
import numpy as np
import faiss
from utils import load_credentials
from sentence_transformers import SentenceTransformer
import pandas as pd

load_credentials()


class RAG:
    def __init__(self, d=768):
        self.index = faiss.IndexHNSWFlat(d, 32)
        self.index.hnsw.efSearch = 100 
        self.index.hnsw.efConstruction = 200
        self.doc_metadata = pd.DataFrame(
            columns=[
                "document_name",
                "chunk_id",
                "content",\
                "project_name",
                "address",
                "type",
                "doc_chunks",
                "project_chunks"
            ]
        )
        
        self.context_index = faiss.IndexHNSWFlat(d, 32)
        self.context_index.hnsw.efSearch = 100 
        self.context_index.hnsw.efConstruction = 200
        self.context_metadata = pd.DataFrame(
            columns=[
                "document_name",
                "chunk_id",
                "content",
                "project_name",
                "address",
                "type",
                "doc_chunks",
                "project_chunks"
            ]
        )
        self.sentence_encoder = SentenceTransformer("jinaai/jina-embeddings-v2-base-code", model_kwargs = {"attn_implementation": "eager"})
        
        self.ignore = {"opioid_crisis_visualization.json"}

    def embed(self, data: pd.DataFrame):
        sentences = [sentence for sentence in data["content"]]
        sentence_embeddings = self.sentence_encoder.encode(sentences).astype(np.float32)
        data["embedding"] = list(sentence_embeddings)
        
    def add(self, data: pd.DataFrame, redo: bool = False):
        if "embedding" not in data.columns or redo:
            self.embed(data)
            
        context_rows = data[data["type"].isin(["md", "tex"])]
        code_rows = data[~data["type"].isin(["md", "tex"])]

        # Add to index
        if not context_rows.empty:
            embeddings = np.vstack(context_rows["embedding"].values).astype(np.float32)
            self.context_index.add(embeddings)
            self.context_metadata = pd.concat([self.context_metadata, context_rows], ignore_index=True)

        if not code_rows.empty:
            embeddings = np.vstack(code_rows["embedding"].values).astype(np.float32)
            self.index.add(embeddings)
            self.doc_metadata = pd.concat([self.doc_metadata, code_rows], ignore_index=True)

    def search(self, query: str, k: int = 20)->pd.DataFrame:
        query_embedding = self.sentence_encoder.encode([query])
        D, I_con = self.context_index.search(query_embedding, k)
        D, I_doc = self.index.search(query_embedding, k)
        return pd.concat([self.context_metadata.iloc[I_con[0]][["project_name", "document_name", "content"]], self.doc_metadata.iloc[I_doc[0]][["project_name", "document_name", "content", "type", "address"]]]).sort_values("project_name")

    def update_metadata(self, data: pd.DataFrame):
        for row in data.iterrows():
            file_type = row[1]["type"]
            if file_type == "md" or file_type == "tex":
                self.context_metadata = pd.concat(
                    [
                        self.context_metadata,
                        row[1][
                            [
                                "document_name",
                                "chunk_id",
                                "content",
                                "project_name",
                                "address",
                                "type",
                                "doc_chunks",
                                "project_chunks",
                            ]
                        ],
                    ],
                    ignore_index=True,
                )
            else:
                self.doc_metadata = pd.concat(
                    [
                        self.doc_metadata,
                        row[1][
                            [
                                "document_name",
                                "chunk_id",
                                "content",
                                "project_name",
                                "address",
                                "type",
                                "doc_chunks",
                                "project_chunks",
                            ]
                        ],
                    ],
                    ignore_index=True,
                )

    def import_data(self, redo = False):
        chunk_count = 0
        for _, _, files in os.walk(os.path.join(script_dir, "data")):
            for file in files:
                if file not in self.ignore:
                    data = pd.DataFrame()
                    with open(os.path.join(script_dir, "data", file), "r") as f:
                        print(f"Loading {file}...")
                        data = pd.read_json(f)
                        chunk_count += len(data)
                        self.add(data, redo)
                    print(f"Saving {file}...")
                    data.to_json(os.path.join(script_dir, "data", file), orient='records')
        print("chunk_count:", chunk_count)


if __name__ == "__main__":
    system = RAG()
    system.import_data()
    print(system.search("What projects use python?"))
