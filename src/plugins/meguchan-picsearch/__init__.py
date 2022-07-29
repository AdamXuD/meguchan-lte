__usage__ = """
惠酱可以以图搜图。
使用方法：
1. 发送 "惠酱搜图" 之后按照惠酱的提示做就可以啦
2. 发送 "惠酱搜上一张图" 即可搜该群发的最后一张图
触发规则：^惠酱搜[图圖]$ ^惠酱搜上一张[图圖]$
"""

__help_version__ = '1.0.0'

__help_plugin_name__ = "惠酱搜图"

import traceback
import re
from typing import Dict
import aiohttp
from aiohttp.client_exceptions import ClientError
from nonebot import get_driver
from nonebot.plugin import on_message, on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.typing import T_State
from nonebot.log import logger

from .config import Config

meguchan_config = Config.parse_obj(get_driver().config.dict())


async def getResult(url: str, mode: str):
    params = {
        "url": url,
        "engine": "ascii2d",
        "secret": meguchan_config.meguchan_secret
    }
    if mode == "iqdb":
        params["engine"] = "iqdb"
    elif mode == "trace":
        params["engine"] = "tracemoe"
    elif mode.startswith("asc"):
        params["engine"] = "ascii2d"
    elif mode == "nao":
        params["engine"] = "saucenao"
    elif mode == "all":
        params["engine"] = "all"

    try:
        async with aiohttp.request(
            "GET",
            f"{meguchan_config.meguchan_api}/picsearch/search",
            params=params
        ) as resp:
            if resp.status == 200:
                res = await resp.json()
                if res["success"] == False:
                    return f"没有找到结果捏：{res['msg']}"
                else:
                    return f"{meguchan_config.meguchan_url}/picsearch/{res['data']['key']}"
            else:
                return "惠酱聪明绝顶的大脑出现了一点点小问题~"
    except:
        logger.warning(traceback.format_exc())
        return "下载出错，请稍后再试"


picsearch = on_regex("^惠酱搜[图圖]$", priority=2)


@picsearch.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    pass


@picsearch.got("mode", prompt="从哪里查找呢? nao/trace/iqdb/ascii2d/all")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    engineList = ["nao", "trace", "iqdb", "ascii2d", "all"]
    if re.match("^[谢謝]+惠酱$", event.message.extract_plain_text()):
        await picsearch.finish("不用谢~")
    elif event.message.extract_plain_text() not in engineList:
        await picsearch.reject("请好好地从里面选一个哦~ nao/trace/iqdb/ascii2d/all\n如想退出搜索模式请发送“谢谢惠酱”")


@picsearch.got("pic", prompt="了解～请发送图片吧！如想退出搜索模式请发送“谢谢惠酱”")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    """
    发现没有的时候要发问
    :return:
    """
    pic = state["pic"][0]
    mode = state["mode"]
    try:
        if pic.type == "image":
            await picsearch.send("正在处理图片")
            msg = await getResult(pic.data["url"], Message(mode).extract_plain_text())
            await picsearch.send(msg)
            await picsearch.finish("搜索完成~")
        elif re.match("^[谢謝]+惠酱$", Message(pic).extract_plain_text()):
            await picsearch.finish("不用谢～")
        else:
            await picsearch.reject("您已经在搜图模式下啦！\n如想退出搜索模式请发送“谢谢惠酱”")
    except (IndexError, ClientError):
        await picsearch.send(traceback.format_exc())
        await picsearch.finish("参数错误")


setu_already_off = on_regex("^[谢謝]+惠酱$", priority=2)


@setu_already_off.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await setu_already_off.finish("にゃ～")


pic_map: Dict[str, str] = {}  # 保存这个群的其中一张色图 {"123456":http://xxx"}


async def check_pic(bot: Bot, event: MessageEvent, state: T_State) -> bool:
    if isinstance(event, MessageEvent):
        for msg in event.message:
            if msg.type == "image":
                url: str = msg.data["url"]
                state["url"] = url
                return True
        return False
    return False


notice_pic = on_message(check_pic, priority=2)


@notice_pic.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    try:
        group_id: str = str(event.group_id)
        pic_map.update({group_id: state["url"]})
    except AttributeError:
        pass


previous = on_regex("^惠酱搜上一张[图圖]$", priority=2)


@previous.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await bot.send(event=event, message="processing...")
    try:
        url: str = pic_map[str(event.group_id)]
        msg = await getResult(url, "all")
        await bot.send(event=event, message=msg)
    except (IndexError, ClientError):
        await bot.send(event, traceback.format_exc())
        await previous.finish("参数错误")
    except KeyError:
        await previous.finish("没有图啊QAQ")
