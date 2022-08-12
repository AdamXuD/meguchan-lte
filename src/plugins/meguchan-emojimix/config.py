import json
from typing import Dict, Optional
import aiohttp
from nonebot import logger
from pydantic import BaseModel, Extra
from pathlib import Path


class Config(BaseModel, extra=Extra.ignore):
    emoji_proxy: Optional[str] = None


data: Dict[str, Dict] = {}


async def initData():
    global data
    path = Path("./data/emoji.json")
    if not path.is_file():
        Path.mkdir(path.parent, parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        try:
            logger.info("正在下载emoji数据。")
            async with aiohttp.request(
                "GET",
                "https://raw.githubusercontent.com/AdamXuD/emoji-kitchen/main/scripts/emojiOutput.json"
            ) as resp:
                if resp.status == 200:
                    d = await resp.text()
                    with open(path, "w") as f:
                        f.write(d)
                    logger.info("下载完成。")
        except:
            logger.warning("network error.")

    try:
        with open(path, "r") as f:
            data.update(json.load(f))
    except:
        logger.warning(
            "emoji.json is not a valid json file."
            + " Please delete it and restart the bot."
        )
