__usage__ = """
惠酱可以缝合两个emoji。
使用方法：
发送任意两个即可。
"""

__help_version__ = '1.0.0'

__help_plugin_name__ = "惠酱emojimix"

import asyncio
import aiohttp
from nonebot import get_driver, on_message
from nonebot.params import T_State
from nonebot.adapters.onebot.v11 import MessageSegment, Event
from nonebot.log import logger
import traceback
import emoji as emojilib


from .config import Config, data, initData

meguchan_config = Config.parse_obj(get_driver().config.dict())
asyncio.get_event_loop().run_until_complete(initData())


API = "https://www.gstatic.com/android/keyboard/emojikitchen/"


def matcher(e: Event, state: T_State) -> bool:
    msg = e.get_plaintext()
    if emojilib.emoji_count(msg) < 2:
        return False
    emojiList = emojilib.emoji_list(msg)
    for key in range(1, len(emojiList)):
        if emojiList[key]["match_start"] == emojiList[key - 1]["match_end"]:
            state["emojis"] = (emojiList[key - 1]["emoji"],
                               emojiList[key]["emoji"])
            return True
    return False


async def mixEmoji(emoji1, emoji2):
    code1 = "-".join([f"{ord(c):x}" for c in emoji1])
    code2 = "-".join([f"{ord(c):x}" for c in emoji2])

    if not data.get(code1):
        return f"不支持的emoji：{emoji1}"
    if not data.get(code2):
        return f"不支持的emoji：{emoji2}"

    url = f"{API}"
    for item in data[code1]:
        if (
            code1 == item["leftEmoji"] and code2 == item["rightEmoji"]
        ) or (
            code2 == item["leftEmoji"] and code1 == item["rightEmoji"]
        ):
            url += f"{item['date']}/u{item['leftEmoji']}/u{item['leftEmoji']}_u{item['rightEmoji']}.png"
            break
    try:
        async with aiohttp.request("GET", url) as resp:
            if resp.status == 200:
                return await resp.read()
        return "出错了，可能不支持该emoji组合"
    except:
        logger.warning(traceback.format_exc())
        return "下载出错，请稍后再试"


emojimix = on_message(matcher)


@emojimix.handle()
async def _(e: Event, state: T_State):
    result = await mixEmoji(*state["emojis"])
    if isinstance(result, str):
        await emojimix.finish(result)
    else:
        await emojimix.finish(MessageSegment.image(result))
