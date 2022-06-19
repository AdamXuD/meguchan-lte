import traceback
import aiohttp
from nonebot import get_driver
from nonebot.log import logger
from nonebot.plugin import on_regex
from nonebot.params import RegexDict
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message, MessageSegment
from nonebot.typing import T_State

from .config import Config


pixiv = on_regex("^惠酱[pP]站(\s)?(?P<pid>\d+)", priority=2)

meguchan_config = Config.parse_obj(get_driver().config.dict())


@pixiv.handle()
async def _(msg: dict = RegexDict()):
    pid = msg["pid"]
    await pixiv.send(f"{meguchan_config.meguchan_url}/pixiv/{pid}")
    await pixiv.finish("搜索完成~")
