import json
file = open('wordlist.txt', 'r', encoding='utf-8')


woordenlijst: list[str] = []
dicta: dict[str,str] = dict()
for line in file:
    woord = line.strip()
    woordenlijst.append(woord)

x = 0

dictv: dict[str,str] = dict()
for woord in woordenlijst:
    if len(woord) > x:
        x = len(woord)
        print(x)
    if woord[:-1] in woordenlijst:
        if woord[:-1] not in dictv:
            dictv[woord[:-1]] = woord[-1]          
        else:
            dictv[woord[:-1]] += woord[-1]



with open('achtervoegselwoorden.json', 'w') as f:
    json.dump(dictv, f, indent=4, sort_keys=True)

"""
for woord in woordenlijst:
    if len(woord) > x:
        x = len(woord)
        print(x)
    if woord[1:] in woordenlijst:
        if woord[1:] not in dicta:
            dicta[woord[1:]] = woord[0]
            
        else:
            dicta[woord[1:]] += woord[0]

with open('voorvoegselwoorden.json', 'w') as f:
    json.dump(dicta, f, indent=4, sort_keys=True)


"""
 