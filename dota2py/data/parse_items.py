import shlex
import pprint
import json


filename = "items.txt"

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
            idx_old = idx
            idx, subdata = parse_substructure(idx + 2, lines)

            # two lines up might be the name, maybe?
            if ((idx_old - 2) < 0):
                data[k] = subdata
            else:
                if COMMENT not in lines[idx_old-2]:
                    #print(f"{idx_old}th line no replacements! [{line}]")
                    data[k] = subdata
                else:
                    #print(f"{idx_old}th line to replace is: {lines[idx_old-2]}")
                    comment_idx = lines[idx_old-2].index(COMMENT)
                    new_name = lines[idx_old - 2][(comment_idx + len(COMMENT)):].strip()
                    #print(f"replacing {k} with {new_name}")
                    data[new_name] = subdata
                    #print(data)

    return (idx, data)


with open(filename) as f:
    lines = f.readlines()
    lines = [line for line in lines if len(line.strip()) != 0]
    idx = 0
    idx, data = parse_substructure(0, lines)
    print("done")
    pprint.pprint(data, depth=2)

    pprint.pprint(list(data.keys()))
    items = data['DOTAAbilities']

    ilist = list()

    for k in items.keys():
        if True: # k.startswith("item_"):
            item = items[k]
            #if 'ItemAliases' not in item:
            #    continue
            name = k #item['ItemAliases']
            if not isinstance(item, dict):
                continue
            id = item['ID']
            id = int(id)
            herodata = dict()
            herodata['name'] = str(k)
            herodata['id'] = id
            ilist.append(herodata)

    output = dict()
    output['result'] = dict()
    output['result']['items'] = ilist
    output['result']['count'] = len(ilist)
    pprint.pprint(output)

    with open("items.json", "w") as outfile:
        json.dump(output, outfile, indent=4)