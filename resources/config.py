import json

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)

PATHS = data["PATHS"]
PREDICTION_PARAMS = data["PREDICTION_PARAMS"]