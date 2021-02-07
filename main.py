#!/usr/bin/env python3
import sys,os,json,re
assert sys.version_info >= (3,9), "This script requires at least Python 3.9"

def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j

def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}


# Removes Harlowe formatting from Twison description
def format_passage(description):
    description = re.sub(r'//([^/]*)//',r'\1',description)
    description = re.sub(r"''([^']*)''",r'\1',description)
    description = re.sub(r'~~([^~]*)~~',r'\1',description)
    description = re.sub(r'\*\*([^\*]*)\*\*',r'\1',description)
    description = re.sub(r'\*([^\*]*)\*',r'\1',description)
    description = re.sub(r'\^\^([^\^]*)\^\^',r'\1',description)
    description = re.sub(r'(\[\[[^\|]*?)\|([^\]]*?\]\])',r'\1->\2',description)
    description = re.sub(r'\[\[([^(->\])]*?)->[^\]]*?\]\]',r'[ \1 ]',description)
    description = re.sub(r'\[\[(.+?)\]\]',r'[ \1 ]',description)
    return description

def update_score(current,score,locations):
    if "score" in current and current["name"] not in locations:
        score += int(current["score"])
    return score

def update(current,choice,game_desc):
    if choice == "":
        return current
    for l in current["links"]:
        if l["name"].lower() == choice:
            current = find_passage(game_desc, l["pid"])
            return current
    print("You got confused. Please try again.")
    return current


def render(current,score):
    print("\n\n")
    print("Fear: {score}".format(score=score))
    print("\n")
    print(current["name"])
    print("\n")
    print(format_passage(current["text"]))
    print("\n")


def get_input():
    choice = input("What would you like to do? (type sleep to end) ")
    choice = choice.lower().strip()
    return choice




def main():
    game_desc = load("game.json")
    current = find_passage(game_desc, game_desc["startnode"])
    last_location = current
    choice = ""

    score = 0
    locations = set()

    while choice != "sleep" and current != {}:
        current = update(current,choice,game_desc)
        score = update_score(current,score,locations)
        locations.add(current["name"])
        render(current,score)
        choice = get_input()

    print("Thanks for playing!")



if __name__ == "__main__":
  main()