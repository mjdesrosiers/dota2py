import shlex
import pprint
import json


filename = "npc_heroes.txt"

data = dict()

COMMENT = "//"

def parse_substructure(idx, lines):
    data = dict()
    while idx < len(lines):
        line = lines[idx]

        #print(line.rstrip(), end="")

        if COMMENT in line:
            comment_idx = line.index(COMMENT)
            line = line[:comment_idx]

        line = line.strip()

        # is this an empty line?
        if not len(line):
            idx += 1
            #print(" | [ COMMENT ]")
            continue

        # is this a name = value?
        parts = shlex.split(line)
        if len(parts) == 2:
            #print(" | [ KEY = VALUE ]")
            k = parts[0]
            v = parts[1]
            data[k] = v
            idx += 1
            continue

        # is this a substructure-end?
        if line is "}":
            #print(" | substructure end")
            idx += 1
            return (idx, data)

        # is this a substructure-start?
        if len(parts) == 1:
            k = parts[0]
            #print(" | key with substructure")
            # check if next line is structure start
            if lines[idx + 1].strip() is not "{":
                raise ValueError("Structure not as expected!")
            idx, subdata = parse_substructure(idx + 2, lines)
            data[k] = subdata

    return (idx, data)


with open(filename) as f:
    lines = f.readlines()
    lines = [line for line in lines if len(line.strip()) != 0]
    idx = 0
    idx, data = parse_substructure(0, lines)
    print("done")
    #pprint.pprint(data)

    heroes = data["DOTAHeroes"]

    hlist = list()

    for k in heroes.keys():
        if k.startswith("npc"):
            hero = heroes[k]
            if 'workshop_guide_name' not in hero:
                continue
            name = hero['workshop_guide_name']
            id = hero['HeroID']
            id = int(id)
            herodata = dict()
            herodata['name'] = str(k)
            herodata['id'] = id
            herodata['localized_name'] = name
            hlist.append(herodata)

    output = dict()
    output['result'] = dict()
    output['result']['heroes'] = hlist
    output['result']['count'] = len(hlist)
    pprint.pprint(output)

    with open("heroes.json", "w") as outfile:
        json.dump(output, outfile, indent=4)