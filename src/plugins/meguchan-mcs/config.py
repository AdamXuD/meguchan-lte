import json
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel, Extra

from nonebot.log import logger


class Config(BaseModel, extra=Extra.ignore):
    meguchan_admin_id: int


class ServerInfo(BaseModel):
    host: str = ""
    rcon_port: int = 0
    rcon_password: str = ""
    name: str = ""
    established_groups: List[int] = []
    managers: List[int] = []


class _ServerItem(BaseModel):
    info: ServerInfo
    status: Optional[bool] = None


serverDict: Dict[str, _ServerItem] = {}
path = None


def appendServer(info, status):
    serverDict.update({
        info.name: _ServerItem.parse_obj({
            "info": info,
            "status": status,
        })
    })
    try:
        with open(path, "w") as f:
            json.dump([item.info.dict() for item in serverDict.values()], f)
    except:
        logger.warning("minecraftServerList.json is not valid.")


def removeServer(name):
    serverDict.pop(name)
    try:
        with open(path, "w") as f:
            json.dump([item.info.dict() for item in serverDict.values()], f)
    except:
        logger.warning("minecraftServerList.json is not valid.")


def initServerDict(p="./data/minecraftServerList.json"):
    global serverDict, path
    path = Path(p)
    if not path.is_file():
        Path.mkdir(path.parent, parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        with open(path, 'w') as f:
            json.dump([], f)

    try:
        with open(path, "r") as f:
            serverDict.update({
                item["name"]: _ServerItem.parse_obj({
                    "info": item,
                    "status": None,
                }) for item in json.load(f)
            })
    except:
        logger.warning("minecraftServerList.json is not a valid json file.")
        serverDict = {}
