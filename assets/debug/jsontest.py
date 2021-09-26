import operator
import json

def sort_scores(Scores):
    return {k: v for k, v in sorted(Scores.items(), key=operator.itemgetter(1), reverse=True)[:10]}

with open('keybinds.json','r') as f:
    Keybinds = json.load(f)

bindup = 101
Keybinds["bindup"] = bindup
print(repr(Keybinds["bindup"]))
# biggest_key = (max(Scores.items(), key=operator.itemgetter(1))[0])
# print(Scores[biggest_key])

# score = 100000000
# if score > Scores[biggest_key]:
#     name = input()
#     Scores[name] = score
#     Scores = sort_scores(Scores)
#     with open('Highscores.json', 'w') as in_file:
#         json.dump(Scores,in_file)
# print(Scores)  # {'key': 'value', 'mynewkey': 'mynewvalue'}
# # print(Scores)
# # data = Scores.items()
# # print(data)
# # keys = Scores.keys()
# # print()
# for name, value in Scores.items():
#     print(f"{name} got: {value}")
