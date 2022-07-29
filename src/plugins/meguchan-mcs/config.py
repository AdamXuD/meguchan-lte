import json
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, Extra

from nonebot.log import logger


class Config(BaseModel, extra=Extra.ignore):
    meguchan_admin_id: int


class ServerInfo(BaseModel):
    host: str = ""
    query_port: int = 0
    rcon_port: int = 0
    rcon_password: str = ""
    name: str = ""
    established_groups: List[int] = []
    managers: List[int] = []


class _ServerItem(BaseModel):
    info: ServerInfo
    status: Optional[bool] = None


serverList: Optional[List[_ServerItem]] = None

path = Path("./data/minecraftServerList.json")
if not path.is_file():
    Path.mkdir(path.parent, parents=True, exist_ok=True)
    path.touch(exist_ok=True)
    with open(path, 'w') as f:
        json.dump([], f)

try:
    with open(path, "r") as f:
        serverList = [_ServerItem.parse_obj({
            "info": item,
            "status": None,
        }) for item in json.load(f)]
except:
    logger.warning("minecraftServerList.json is not a valid json file.")
    serverList = []


def appendServer(info, status):
    serverList.append(_ServerItem.parse_obj({
        "info": info,
        "status": status,
    }))
    with open(path, "w") as f:
        json.dump([server.info.dict() for server in serverList], f)


def removeServer(obj):
    serverList.remove(obj)
    with open(path, "w") as f:
        json.dump([server.info.dict() for server in serverList], f)
