import json
import pandas as pd
import gspread
import statsmodels.stats.inter_rater as irr
import matplotlib.pyplot as plt

filenames = [
    "project-2-at-2024-05-03-18-22-da5d8ca1.json",
    "project-5-at-2024-04-28-02-09-d9ec588d.json",
    "project-13-at-2024-05-05-17-51-ba15127f.json",
    "project-17-at-2024-05-05-16-17-d3c3de99.json",
]

docs_for_four_annotators = set()

file = open("project-2-at-2024-05-03-18-22-da5d8ca1.json", encoding="utf-8")

for f in json.load(file):
    docs_for_four_annotators.add(f["data"]["text"])

file.close()

clause_type_dict = {
    "Declarative Clause": 0,
    "Interrogative Clause": 1,
    "Imperative Clause": 2,
    "Exclamatory Clause": 3,
}
speech_act_dict = {
    "Offer": 0,
    "Promise": 1,
    "Request": 2,
    "Order": 3,
    "Prompt": 4,
    "Explain": 5,
    "Statement": 6,
    "Clarification": 7,
    "Open-ended": 8,
    "Closed-ended": 9,
    "Confirmation": 10,
    "Rhetorical": 11,
    "Response": 12,
    "Open-ended Declaration": 13,
    "Warning": 14,
}
broad_speech_act_dict = {"Commissive": 0, "Directive": 1, "Inform": 2, "Question": 3}

commissives = {"Offer", "Promise"}
directives = {"Request", "Order", "Prompt"}
informs = {"Explain", "Statement", "Response", "Open-ended Declaration"}
questions = {
    "Clarification",
    "Open-ended",
    "Closed-ended",
    "Confirmation",
    "Rhetorical",
}

turn_counts = []
dialogue_act_counts = []
broad_dialogue_act_counts = []
clause_type_counts = []

clause_type_list = []
speech_act_list = []
broad_speech_acts_list = []
turn_sets = []
for filename in filenames:
    turns = set()
    clause_types = {}
    speech_acts = {}
    broad_speech_acts = {}
    clause_type_count = [0, 0, 0, 0]
    dialogue_act_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    broad_dialogue_act_count = [0, 0, 0, 0]
    data = json.load(open(filename, encoding="utf-8"))
    for f in data:
        if f["data"]["text"] in docs_for_four_annotators:
            for item in f["annotations"]:
                for result in item["result"]:
                    start = result["value"]["start"]
                    end = result["value"]["end"]
                    text = result["value"]["text"]
                    turn = (start, end, text)
                    if "labels" in result["value"]:
                        turns.add(turn)
                    elif (
                        "choices" in result["value"]
                        and result["value"]["choices"][0] in clause_type_dict
                    ):
                        clause_types[turn] = result["value"]["choices"][0]
                        clause_type_count[
                            clause_type_dict[result["value"]["choices"][0]]
                        ] += 1
                    elif (
                        "choices" in result["value"]
                        and result["value"]["choices"][0] in speech_act_dict
                    ):
                        speech_acts[turn] = result["value"]["choices"][0]
                        dialogue_act_count[
                            speech_act_dict[result["value"]["choices"][0]]
                        ] += 1
                        if result["value"]["choices"][0] in commissives:
                            broad_speech_acts[turn] = "Commissive"
                            broad_dialogue_act_count[0] += 1
                        elif result["value"]["choices"][0] in directives:
                            broad_speech_acts[turn] = "Directive"
                            broad_dialogue_act_count[1] += 1
                        elif result["value"]["choices"][0] in informs:
                            broad_speech_acts[turn] = "Inform"
                            broad_dialogue_act_count[2] += 1
                        elif result["value"]["choices"][0] in questions:
                            broad_speech_acts[turn] = "Question"
                            broad_dialogue_act_count[3] += 1
                        else:
                            print("error:", turn, result["value"]["choices"][0])
                    else:
                        print("error:", turn, result["value"]["choices"][0])

    turn_sets.append(turns)
    turn_counts.append(len(turns))
    clause_type_counts.append(clause_type_count)
    dialogue_act_counts.append(dialogue_act_count)
    broad_dialogue_act_counts.append(broad_dialogue_act_count)
    clause_type_list.append(clause_types)
    speech_act_list.append(speech_acts)
    broad_speech_acts_list.append(broad_speech_acts)

for i in range(4):
    print("Annotator " + str(i + 1) + ":")
    print("total turns annotated:", turn_counts[i])
    print("---------------------------------")
    print("no. of declarative clauses annotated:", clause_type_counts[i][0])
    print("no. of interrogative clauses annotated:", clause_type_counts[i][1])
    print("no. of imperative clauses annotated:", clause_type_counts[i][2])
    print("no. of exclamatory clauses annotated:", clause_type_counts[i][3])
    print("---------------------------------")
    print('no. of "offer" tags labeled:', dialogue_act_counts[i][0])
    print('no. of "promise" tags labeled:', dialogue_act_counts[i][1])
    print('no. of "request" tags labeled:', dialogue_act_counts[i][2])
    print('no. of "order" tags labeled:', dialogue_act_counts[i][3])
    print('no. of "prompt" tags labeled:', dialogue_act_counts[i][4])
    print('no. of "warning" tags labeled:', dialogue_act_counts[i][14])
    print('no. of "explain" tags labeled:', dialogue_act_counts[i][5])
    print('no. of "statement" tags labeled:', dialogue_act_counts[i][6])
    print('no. of "open-ended declaration" tags labeled:', dialogue_act_counts[i][13])
    print('no. of "response" tags labeled:', dialogue_act_counts[i][12])
    print('no. of "clarification" tags labeled:', dialogue_act_counts[i][7])
    print('no. of "open-ended" tags labeled:', dialogue_act_counts[i][8])
    print('no. of "closed-ended" tags labeled:', dialogue_act_counts[i][9])
    print('no. of "confirmation" tags labeled:', dialogue_act_counts[i][10])
    print('no. of "rhetorical" tags labeled:', dialogue_act_counts[i][11])
    print("---------------------------------")
    print('no. of "commissive" tags labeled:', broad_dialogue_act_counts[i][0])
    print('no. of "directive" tags labeled:', broad_dialogue_act_counts[i][1])
    print('no. of "inform" tags labeled:', broad_dialogue_act_counts[i][2])
    print('no. of "question" tags labeled:', broad_dialogue_act_counts[i][3])
    print("---------------------------------\n\n")

clause_type_order = [
    "Declarative clause",
    "Interrogative clause",
    "Imperative clause",
    "Exclamatory clause",
]
clause_type_totals = [
    sum(clause_type_counts[i][j] for i in range(len(clause_type_counts)))
    for j in range(len(clause_type_order))
]
dialogue_act_order = [
    "Offer",
    "Promise",
    "Request",
    "Order",
    "Prompt",
    "Explain",
    "Statement",
    "Clarification",
    "Open-ended",
    "Closed-ended",
    "Confirmation",
    "Rhetorical",
    "Response",
    "Open-ended Declaration",
    "Warning",
]
dialogue_act_totals = [
    sum(dialogue_act_counts[i][j] for i in range(len(dialogue_act_counts)))
    for j in range(len(dialogue_act_order))
]
broad_order = ["Commissive", "Directive", "Inform", "Question"]
broad_totals = [
    sum(broad_dialogue_act_counts[i][j] for i in range(len(broad_dialogue_act_counts)))
    for j in range(len(broad_order))
]

print(clause_type_totals)
print(dialogue_act_totals)
print(broad_totals)

fig = plt.figure(figsize=(6, 4))
plt.xticks(rotation=20, ha="right")
plt.bar(clause_type_order, clause_type_totals, color="maroon", width=0.4)
plt.xlabel("Clause Type")
plt.ylabel("Count")
plt.title("Total Counts of Clause Type Labels")
plt.tight_layout()
plt.show()

fig = plt.figure(figsize=(10, 5))
plt.xticks(rotation=30, ha="right")
plt.bar(dialogue_act_order, dialogue_act_totals, color="mediumaquamarine", width=0.4)
plt.xlabel("Dialogue Act")
plt.ylabel("Count")
plt.title("Total Counts of Dialogue Act Labels")
plt.tight_layout()
plt.show()

fig = plt.figure(figsize=(6, 4))
plt.bar(broad_order, broad_totals, color="goldenrod", width=0.4)
plt.xlabel("Broad Dialogue Act")
plt.ylabel("Count")
plt.title("Total Counts of Broad Dialogue Act Labels")
plt.show()

turns_union = turn_sets[0].union(turn_sets[1], turn_sets[2], turn_sets[3])
turns_intersection = turn_sets[0].intersection(turn_sets[1], turn_sets[2], turn_sets[3])

turn_agreement_matrix = [[0, 0] for i in range(len(turns_union))]
turn_order = []
for i, turn in enumerate(turns_union):
    turn_order.append(turn)
    for turn_set in turn_sets:
        if turn in turn_set:
            turn_agreement_matrix[i][0] += 1
        else:
            turn_agreement_matrix[i][1] += 1


clause_type_agreement_matrix = [[0, 0, 0, 0, 0] for i in range(len(turns_intersection))]
speech_act_agreement_matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(turns_intersection))
]
broad_speech_act_agreement_matrix = [
    [0, 0, 0, 0, 0] for i in range(len(turns_intersection))
]
clause_speech_act_turn_order = []
for i, turn in enumerate(turns_intersection):
    clause_speech_act_turn_order.append(turn)
    for clause_types in clause_type_list:
        try:
            clause_type_agreement_matrix[i][clause_type_dict[clause_types[turn]]] += 1
        except KeyError:
            clause_type_agreement_matrix[i][
                len(clause_type_agreement_matrix[i]) - 1
            ] += 1
    for speech_acts in speech_act_list:
        try:
            speech_act_agreement_matrix[i][speech_act_dict[speech_acts[turn]]] += 1
        except KeyError:
            speech_act_agreement_matrix[i][len(speech_act_agreement_matrix[i]) - 1] += 1
    for broad_speech_acts in broad_speech_acts_list:
        try:
            broad_speech_act_agreement_matrix[i][
                broad_speech_act_dict[broad_speech_acts[turn]]
            ] += 1
        except KeyError:
            broad_speech_act_agreement_matrix[i][
                len(broad_speech_act_agreement_matrix[i]) - 1
            ] += 1


print(
    "turns agreed on by 3 annotators:",
    str(len(turns_intersection)) + "/" + str(len(turns_union)),
    "=",
    len(turns_intersection) / len(turns_union),
)
print(
    "fleiss kappa for clause type:\tk =", irr.fleiss_kappa(clause_type_agreement_matrix)
)
print(
    "fleiss kappa for speech act type:\tk =",
    irr.fleiss_kappa(speech_act_agreement_matrix),
)
print(
    "fleiss kappa for broad speech act type:\tk =",
    irr.fleiss_kappa(broad_speech_act_agreement_matrix),
)


adjusted_turn_sets = []
for turn_set in turn_sets:
    turns = set()
    for turn in turn_set:
        text = turn[2]
        end = turn[1]
        if text.endswith("."):
            text = text.rstrip(".")
            end -= 1
        turns.add((turn[0], end, text))
    adjusted_turn_sets.append(turns)

turns_union = adjusted_turn_sets[0].union(
    adjusted_turn_sets[1], adjusted_turn_sets[2], adjusted_turn_sets[3]
)
turns_intersection = adjusted_turn_sets[0].intersection(
    adjusted_turn_sets[1], adjusted_turn_sets[2], adjusted_turn_sets[3]
)

turn_agreement_matrix = [[0, 0] for i in range(len(turns_union))]
turn_order = []
for i, turn in enumerate(turns_union):
    turn_order.append(turn)
    for turn_set in turn_sets:
        if turn in turn_set:
            turn_agreement_matrix[i][0] += 1
        else:
            turn_agreement_matrix[i][1] += 1


clause_type_agreement_matrix = [[0, 0, 0, 0, 0] for i in range(len(turns_intersection))]
speech_act_agreement_matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(turns_intersection))
]
broad_speech_act_agreement_matrix = [
    [0, 0, 0, 0, 0] for i in range(len(turns_intersection))
]
clause_speech_act_turn_order = []
for i, turn in enumerate(turns_intersection):
    clause_speech_act_turn_order.append(turn)
    for clause_types in clause_type_list:
        try:
            clause_type_agreement_matrix[i][clause_type_dict[clause_types[turn]]] += 1
        except KeyError:
            clause_type_agreement_matrix[i][
                len(clause_type_agreement_matrix[i]) - 1
            ] += 1
    for speech_acts in speech_act_list:
        try:
            speech_act_agreement_matrix[i][speech_act_dict[speech_acts[turn]]] += 1
        except KeyError:
            speech_act_agreement_matrix[i][len(speech_act_agreement_matrix[i]) - 1] += 1
    for broad_speech_acts in broad_speech_acts_list:
        try:
            broad_speech_act_agreement_matrix[i][
                broad_speech_act_dict[broad_speech_acts[turn]]
            ] += 1
        except KeyError:
            broad_speech_act_agreement_matrix[i][
                len(broad_speech_act_agreement_matrix[i]) - 1
            ] += 1


print(
    "\n\nadjusted turns agreed on by 3 annotators:",
    str(len(turns_intersection)) + "/" + str(len(turns_union)),
    "=",
    len(turns_intersection) / len(turns_union),
)
print(
    "fleiss kappa for clause type:\tk =", irr.fleiss_kappa(clause_type_agreement_matrix)
)
print(
    "fleiss kappa for speech act type:\tk =",
    irr.fleiss_kappa(speech_act_agreement_matrix),
)
print(
    "fleiss kappa for broad speech act type:\tk =",
    irr.fleiss_kappa(broad_speech_act_agreement_matrix),
)

"""
sa = gspread.service_account(filename='service_account.json')
sheet_name = 'Annotations'
worksheet_name = 'Turn Agreement'
sheet = sa.open(sheet_name)
try:
    worksheet = sheet.worksheet(worksheet_name)
except Exception:
    sheet.add_worksheet(worksheet_name, 1000, 5)
    worksheet = sheet.worksheet(worksheet_name)
worksheet.update('A1:E1', [['start', 'end', 'text', 'labeled turn', 'didn\'t label turn']])
rang = len(turns_union) + 1
data = [list(turn_order[i]) + (turn_agreement_matrix[i]) for i in range(rang - 1)]
worksheet.update('A2:E' + str(rang), data)

worksheet_name = 'Clause Type Agreement'
try:
    worksheet = sheet.worksheet(worksheet_name)
except Exception:
    sheet.add_worksheet(worksheet_name, 1000, 8)
    worksheet = sheet.worksheet(worksheet_name)
worksheet.update('A1:H1', [['start', 'end', 'text', 'Declarative', 'Interrogative', 'Imperative', 'Exclamatory',
                            'No Clause Type']])
rang = len(turns_intersection) + 1
data = [list(clause_speech_act_turn_order[i]) + (clause_type_agreement_matrix[i]) for i in range(rang - 1)]
worksheet.update('A2:H' + str(rang), data)

worksheet_name = 'Speech Act Agreement'
try:
    worksheet = sheet.worksheet(worksheet_name)
except Exception:
    sheet.add_worksheet(worksheet_name, 1000, 15)
    worksheet = sheet.worksheet(worksheet_name)
worksheet.update('A1:R1', [['start', 'end', 'text', 'Offer', 'Promise', 'Request', 'Order', 'Prompt', 'Explain',
                            'Statement', 'Clarification', 'Open-ended', 'Closed-ended', 'Confirmation', 'Rhetorical',
                            'Response', 'Open-ended Declaration', 'No Speech Act']])
rang = len(turns_intersection) + 1
data = [list(clause_speech_act_turn_order[i]) + (speech_act_agreement_matrix[i]) for i in range(rang - 1)]
worksheet.update('A2:R' + str(rang), data)

worksheet_name = 'Broad Speech Act Agreement'
try:
    worksheet = sheet.worksheet(worksheet_name)
except Exception:
    sheet.add_worksheet(worksheet_name, 1000, 8)
    worksheet = sheet.worksheet(worksheet_name)
worksheet.update('A1:H1', [['start', 'end', 'text', 'Commissive', 'Directive', 'Inform', 'Question',
                            'No Speech Act']])
rang = len(turns_intersection) + 1
data = [list(clause_speech_act_turn_order[i]) + (broad_speech_act_agreement_matrix[i]) for i in range(rang - 1)]
worksheet.update('A2:H' + str(rang), data)



#The code below is to enter the annotations into a google spreadsheet
df_list = []
for filename in filenames:
    data = json.load(open(filename, encoding="utf-8"))
    data_dict = {}
    data_dict['file'] = []
    data_dict['id'] = []
    data_dict['start'] = []
    data_dict['end'] = []
    data_dict['tag'] = []
    data_dict['text'] = []
    current_file = 0
    for file in data:
        current_file += 1
        for i, item in enumerate(file['annotations']):
            for result in item['result']:
                start = result['value']['start']
                end = result['value']['end']
                text = result['value']['text']
                id = result['id']
                print("id:", result['id'])
                print("start:", result['value']['start'], "end:", result['value']['end'])
                data_dict['file'].append(str(current_file))
                data_dict['start'].append(start)
                data_dict['end'].append(end)
                data_dict['id'].append(id)
                data_dict['text'].append(text)
                try:
                    label = result['value']['labels']
                    print("label:", result['value']['labels'])
                    data_dict['tag'].append(label)
                except KeyError:
                    choice = result['value']['choices']
                    print("Choice:", result['value']['choices'])
                    data_dict['tag'].append(choice)

    df_list.append(pd.DataFrame(data_dict, dtype=str))



sa = gspread.service_account(filename='service_account.json')
sheet_name = 'Annotations'
worksheet_names = ['IAAannotations1', 'IAAannotations2', 'IAAannotations3', 'IAAannotations4']
sheet = sa.open(sheet_name)

for df, worksheet_name in zip(df_list, worksheet_names):

    try:
        worksheet = sheet.worksheet(worksheet_name)
    except Exception:
        sheet.add_worksheet(worksheet_name, 1000, 5)
        worksheet = sheet.worksheet(worksheet_name)

    worksheet.update('A1:E1', [['file', 'start', 'end', 'tag', 'text']])
    rang = len(df['start'])
    data = [[df['file'][i], df['start'][i], df['end'][i], ''.join(df['tag'][i]), df['text'][i]] for i in range(0, rang)]
    worksheet.update('A2:E' + str(rang + 1), data)
"""
