# from transformers import pipeline
import rag
import os
from typing import List
from ollama import chat
import pandas as pd
# IDEAS:
# 

SYSTEM_PROMPT = """
<<SYS>>
You are a helpful project expert. You are to pose as the author of all of the presented documents. You know everything there is about the documents provided to you and how to provide clarifying explanations about them. You must answer as straightforwardly as possible and highlight important parts of the codebase and the reasoning behind it.
For each response, please provide the excerpts that are the most relevant in your opinion, where they are in the code base, and what other documents the user should look at.

Before responding, you must determine what documents provided are relevant. You must phrase your response using only the relevant documents. Do not reveal information about the documents that are not relevant.
If you don't know how to answer the question, please say I don't know. If the question doesn't require the provided documents, please choose not to talk about them.
<</SYS>>
"""

class ChatLLM:
    def __init__(self):
        # self.chat = pipeline(task="text-generation", model="mistralai/Mistral-7B-Instruct-v0.3")
        self.rag = rag.RAG()
        self.rag.import_data()

    def retrieve(self, message):
        prompt = f"Provide list of keywords that summarizes of what the query is looking for in a codebase. For example, the language used, the libraries used, the type of project, the README, etc. If the question isn't asking anything about code, you must respond with nothing. Your answer must strictly follow the format: Answer: keyword1, keyword2, ...\n Query: {message["content"]}"
        response = chat(model = "mistral:instruct", messages= [{"role":"user", "content": prompt}])
        result = response["message"]["content"]\
                .split("Answer:")[-1]\
                .split("</think>")[-1]\
                .strip()
        if not result:
            return ""
        results = self.rag.search(result)
        return results
    
    def format_retrieved(self, data: pd.DataFrame):
        prompt = ""
        template = """Project Name: {name}
        Document: {doc}
            Path: {path}
            Type: {type}
            Content: \'{text}\'
        
        """
        for row in data.iterrows():
            prompt+=template.format(name = row[1]["project_name"],
                                    doc = row[1]["document_name"],
                                    path = row[1]["address"],
                                    type = row[1]["type"],
                                    text = row[1]["content"])
        return prompt
            

    def generate(self, messages: List[dict], project = ""):
        if messages:
            results = self.retrieve(messages[-1])
            results = self.format_retrieved(results)
            # print(results)
            prompt = f"Relevant documents:\n {results} Please answer the following question about the documents: {messages[-1]["content"]}. Please provide explanation and be willing to provide more information. If the input is not a question, please respond accordingly."
            response = chat(model = "mistral:instruct", messages= [{"role":"system", "content": SYSTEM_PROMPT}]+messages[:-1]+[{"role":"user", "content":prompt}])
            result = response["message"]["content"]
            return result
            # return response[0]["generated_text"][len(prompt) :].strip()

    def run(self):
        messages = []
        os.system("cls" if os.name == "nt" else "clear")
        print(
            "Welcome to the project information system! What do you want to know about my projects?"
        )
        usr_input = ""
        while usr_input != "bye":
            usr_input = input("================ User Message ================\n")
            messages.append({"role": "user", "content": usr_input})
            print("================ Response ================")
            response = self.generate(messages)
            print(response)
            response = messages.append({"role": "assistant", "content": response})
