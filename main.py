# -*- coding: utf-8 -*-

import requests
import json


url = "https://api.cloud.my.games/api/games?page=1&page_size=100"
path = "games.json"
data = list()

while True:

    response = requests.get(url).json()

    for item in response["results"]:
        launchers = [{"id": _item["id"], "launcher": _item["launcher"]}
                     for _item in item["game_launchers"]]

        data.append({
            "launchers": launchers,
            "name": item["name"],
            "plans": [_item["name"] for _item in item["plans_family"]],
        })

    url = response["next"]

    if not url:
        break

with open(path, 'w', encoding="UTF-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4, sort_keys=True)
