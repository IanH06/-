import json
import getFunctions

def deckToDict(DID,fileName):
    fileName += ".json"
    deckInfo = (getFunctions.getDeckInfo(DID))
    notes = (getFunctions.getNotes(DID))

    dict = {"deckName":deckInfo[2], "Summary":deckInfo[3], "Notes":notes}

    with open(fileName, "w") as wr:
        json.dump(dict, wr)

def loadJson(fileName):
    try:
        with open(fileName + ".json", "r") as r:
            print(fileName)
            x = json.load(r)

    except FileNotFoundError:
        print("The file does not exist!")
        return "FileNotFound"
    
    else:
        return x

    