import json


def load_catalog():
    with open("data/catalog.json", "r", encoding="utf-8") as f:
        return json.load(f)