#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
import mypy
import json
from dotenv import load_dotenv

__config = {}


def __load_config() -> None:
    global __config
    with open("config.json", 'r') as f:
        __config = json.loads(f.read())


def get_config(key: str):
    if len(__config) == 0:
        load_dotenv()
        __load_config()
    return __config[key]