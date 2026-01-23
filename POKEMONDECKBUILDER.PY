from io import BytesIO
from PIL import Image
import requests
import json
import os
from pathlib import Path


def loadCards(jsonFile):
    if jsonFile.exists():
        with open(jsonFile, "r") as f:
            return json.load(f)
    return {"Main Storage": [], "Deck Lists": []}


def openurl(card):
    families = ['sv', 'me']
    names = {
        "sv": {
            "SV1": "sv01", 'SVI': "sv01", "PAL": "sv02", "OBF": "sv03", "MEW": "sv03.5",
            "SVP": "svp", "PAR": "sv04", "PAF": "sv04.5", "TEF": "sv05",
            "TWM": "sv06", "SFA": "sv06.5", "SCR": "sv07", "SSP": "sv08",
            "PRE": "sv08.5", "JTG": "sv09", "DRI": "sv10", "WHT": "sv10.5w",
            "BLK": "sv10.5b"
        },
        "me": {
            "MEG": "me01", "PFL": "me02"
        }
    }

    # url2 = "https://assets.tcgdex.net/en/sv/sv02/001/low.png"
    # url = "https://assets.tcgdex.net/en/me/me02/001/low.png"
    setCode = card["CardSet"]
    num = str(card["CardNumber"]).zfill(3)
    if setCode == 'MEE' or setCode == 'SVE':
        return "https://assets.tcgdex.net/en/sv/sv02/001/low.png"
    else:
        if setCode in names['sv']:
            family = families[0]
            mapped = names['sv'][setCode]
        elif setCode in names['me']:
            family = families[1]
            mapped = names['me'][setCode]
        else:
            raise ValueError(f"Set not recognized: {setCode}")

        url = f"https://assets.tcgdex.net/en/{family}/{mapped}/{num}/high.png"
        return url


def listopenurl(cardList):
    linkList = []
    for card in cardList:
        linkList.append([openurl(card), card])
    return linkList


def saveCards(cards, jsonFile):
    with open(jsonFile, "w") as f:
        json.dump(cards, f, indent=4)


def inputcards(StorageOption, jsonFile, vals):
    cards = loadCards(jsonFile)
    cardstr = vals[0]
    cardset = vals[1]
    if len(cardset) != 3:
        return
    try:
        int(vals[2])
    except Exception:
        return
    cardnm = vals[2]
    try:
        int(vals[3])
    except Exception:
        return
    existing = next(
        (c for c in cards[StorageOption] if c["CardName"].lower() == cardstr.lower()
         and c["CardSet"].lower() == cardset.lower()
         and c["CardNumber"] == int(cardnm)),
        None
    )
    if existing:
        existing["Amount"] += int(vals[3])
    else:
        new_card = {
            "CardName": cardstr,
            "CardSet": cardset,
            "CardNumber": int(cardnm),
            "Amount": int(vals[3])
        }
        cards[StorageOption].append(new_card)

    saveCards(cards, jsonFile)


def addOrRemove(StorageOption, jsonFile, vals, oneOrZero):
    precards = loadCards(jsonFile)
    cards = precards
    if oneOrZero == 1:
        for card in cards[StorageOption]:
            if card["CardName"] == vals[0] and card["CardSet"] == vals[1] and card["CardNumber"] == vals[2]:
                card["Amount"] += 1
    else:
        for card in cards[StorageOption]:
            if card["CardName"] == vals[0] and card["CardSet"] == vals[1] and card["CardNumber"] == vals[2]:
                card["Amount"] -= 1
            if card["Amount"] == 0:
                newCards = []
                for card in cards[StorageOption]:
                    if card["Amount"] != 0:
                        newCards += [card]
                cards[StorageOption] = newCards

    saveCards(cards, jsonFile)
