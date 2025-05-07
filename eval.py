from rouge_score import rouge_scorer
import chat
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
from tqdm import tqdm

macro = {"rouge1":[0,0,0], "rouge2":[0,0,0], "rougeL":[0,0,0]}

model = chat.ChatLLM()
scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer = True)
count = 0
with open(os.path.join(script_dir, "test_questions.tab.tsv"), "r") as f:
    for line in tqdm(f):
        prompt, answer = line.split("\t")
        response = model.generate([{"role":"user", "content": prompt}])
        count += 1
        scores = scorer.score(answer, response)
        for key, values in scores.items():
            values = [values.precision, values.recall, values.fmeasure]
            macro[key] = [curr+new for curr, new in zip(values, macro[key])]

for key, values in macro.items():
    macro[key] = [curr/count for curr in values]
print(macro)