# -*- coding: utf-8 -*-

from json import dump
from typing import List, NamedTuple, Tuple

from requests import Session

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
            id=game.get('id'),
            name=game.get('name'),
            description=game.get('long_descr'),
            plans=tuple(rate.get('name') for rate in game.get('plans_family')),
            launchers=tuple(
                Launcher(id=item.get('id'), name=item.get('launcher'))
                for item in game.get('game_launchers')
            )
        )
        for game in games_dict
    ]


def main() -> None:
    session = Session()
    
    url = f'{API_URL}/api/games'
    params = {
    	"page_size": 100
    }
    response = session.get(url, params=params).json()

    count = response.get('count')
    games: List[Game] = validate_game(response.get('results'))

    for _ in range(100, count, 100):
        url = response.get('next')
        response = session.get(url).json()
        games.extend(
            validate_game(response.get('results'))
        )


    with open("games.json", 'w', encoding="UTF-8") as file:
        dump(
            [item._asdict() for item in games],
            file,
            indent=4,
            sort_keys=True,
            ensure_ascii=False,
        )

if __name__ == '__main__':
    main()
