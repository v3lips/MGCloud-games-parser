# -*- coding: utf-8 -*-

from json import dump
from typing import List, NamedTuple, Tuple

import requests

API_URL = "https://api.cloud.my.games"


class Launcher(NamedTuple):
    id: int
    name: str


class Game(NamedTuple):
    id: int
    name: str
    description: str
    plans: Tuple[str]
    launchers: Tuple[str]


def validate_game(games_dict: dict) -> Tuple[Game]:
    return [
        Game(
            id=meta.get('id'),
            name=meta.get('name'),
            description=meta.get('long_descr'),
            plans=tuple(rate.get('name') for rate in meta.get('plans_family')),
            launchers=tuple(
                Launcher(id=item.get('id'), name=item.get('launcher'))
                for item in meta.get('game_launchers')
            )
        )
        for meta in games_dict
    ]


def main() -> None:
    url = f'{API_URL}/api/games?page_size=100'
    response = requests.get(url).json()

    count = response.get('count')
    games: List[Game] = validate_game(response.get('results'))

    for _ in range(100, count, 100):
        url = response.get('next')
        response = requests.get(url).json()
        games.extend(
            validate_game(response.get('results'))
        )


    with open("path.json", 'w', encoding="UTF-8") as file:
        dump(
            [item._asdict() for item in games],
            file,
            indent=4,
            sort_keys=True,
            ensure_ascii=False,
        )

if __name__ == '__main__':
    main()

