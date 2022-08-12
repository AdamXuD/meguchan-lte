__usage__ = """
惠酱可以检测mc服务器的情况。
使用方法：
1. 发送 "/mc dels <服务器名称>" 可向惠酱删除服务器（仅指定的管理员可使用）。
2. 发送 "/mc check <服务器名称>" 可检测服务器状态。
3. 发送 "/mc list" 可查看本群或由您管理的服务器列表。
"""

__help_version__ = '1.0.0'

__help_plugin_name__ = "惠酱mc"


import json
import time
from typing import List, Optional
from html import unescape

from aiomcrcon import Client
import nonebot
from nonebot.plugin import require, on_regex
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import RegexDict

from .config import ServerInfo, Config, appendServer, initServerDict, removeServer, serverDict


scheduler = require("nonebot_plugin_apscheduler").scheduler
meguchan_config = Config.parse_obj(nonebot.get_driver().config.dict())
initServerDict()


async def pingServer(host: str, queryPort: int, password: str):
    startTime = time.time()
    try:
        async with Client(host, queryPort, password):
            return (time.time() - startTime) / 2, True
    except:
        return -1, False


def createMsg(title: str, info: ServerInfo, status: bool, ping: float, other: Optional[str] = None):
    return (
        f"【{title}】\n"
        + f"Name: {info.name}\n"
        + f"Host: {info.host}\n"
        + f"Status: {'On' if status else 'Off'}"
        + (f"\nPing: {round(ping * 1000, 3)}ms" if status else "")
        + (f"\n{other}" if other else "")
    )


def getManagers(managers: List[int]):
    return [meguchan_config.meguchan_admin_id] + managers


@scheduler.scheduled_job("cron", minute="*/1", id="mcstatus")
async def _():
    try:
        bot = nonebot.get_bot()
    except:
        return

    for item in serverDict.values():
        ping, status = await pingServer(
            item.info.host,
            item.info.rcon_port,
            item.info.rcon_password
        )
        if item.status == None:
            item.status = status
            continue
        if item.status == status:
            continue

        item.status = status
        message = createMsg("服务器状态发生变化", item.info, status, ping)
        for group in item.info.established_groups:
            await bot.send_msg(
                group_id=group,
                message=message,
            )
        for manager in getManagers(item.info.managers):
            await bot.send_msg(
                user_id=manager,
                message=message,
            )


fetchTemplate = on_regex("^/mc template$")


@fetchTemplate.handle()
async def _():
    await fetchTemplate.finish(ServerInfo().json())


addServer = on_regex("^/mc adds `(?P<info>.*)`")


@addServer.handle()
async def _(event: MessageEvent, msg: dict = RegexDict()):
    if event.user_id != meguchan_config.meguchan_admin_id:
        return await addServer.finish("你不是惠酱管理员，不能添加服务器~")

    info = unescape(msg["info"])

    try:
        info = ServerInfo.parse_obj(json.loads(info))
        if serverDict.get(info.name):
            return await addServer.finish("同名服务器已存在~")
        ping, status = await pingServer(
            info.host,
            info.rcon_port,
            info.rcon_password
        )
        appendServer(info, status)
        message = createMsg("服务器添加成功", info, status, ping)
    except:
        message = "无效的服务器信息"

    return await addServer.finish(message)


deleteServer = on_regex("^/mc dels (?P<name>[a-zA-Z0-9]*)$")


@deleteServer.handle()
async def _(event: MessageEvent, msg: dict = RegexDict()):
    name = msg["name"]

    if item := serverDict.get(name):
        managers = getManagers(item.info.managers)
        if event.user_id not in managers:
            return await deleteServer.finish("你不是该服务器管理员，不能删除该服务器~")
        else:
            removeServer(name)
            return await deleteServer.finish("服务器删除成功~")

    return await deleteServer.finish("服务器不存在~")


checkStatus = on_regex("^/mc check (?P<name>[a-zA-Z0-9]*)$")


@checkStatus.handle()
async def _(msg: dict = RegexDict()):
    name = msg["name"]

    if item := serverDict.get(name):
        try:
            startTime = time.time()
            async with Client(
                item.info.host,
                item.info.rcon_port,
                item.info.rcon_password
            ) as c:
                ping, status = (time.time() - startTime) / 2, True
                other = (await c.send_cmd("list"))[0]
        except:
            ping, status, other = -1, False, None

        return await checkStatus.finish(
            createMsg(
                "服务器状态如下",
                item.info,
                status,
                ping,
                other
            )
        )

    return await checkStatus.finish("服务器不存在~")


listServer = on_regex("^/mc list$")


@listServer.handle()
async def _(event: MessageEvent):
    message = ("【订阅的服务器列表】\n")

    for item in serverDict.values():
        if isinstance(
            event, GroupMessageEvent
        ) and (event.group_id not in item.info.established_groups):
            continue
        if isinstance(
            event, PrivateMessageEvent
        ) and (event.user_id not in getManagers(item.info.managers)):
            continue

        ping, status = await pingServer(
            item.info.host,
            item.info.rcon_port,
            item.info.rcon_password
        )
        message += f"{createMsg('=====', item.info, status, ping)}\n"

    return await listServer.finish(message)


executeCmd = on_regex("^/mc exec (?P<name>[a-zA-Z0-9]*) `(?P<cmd>.*)`$")


@executeCmd.handle()
async def _(event: MessageEvent, msg: dict = RegexDict()):
    cmd = msg["cmd"]
    name = msg["name"]

    if item := serverDict.get(name):
        if event.user_id not in getManagers(item.info.managers):
            return await addServer.finish("您未被指定为该服务器管理员，不能使用命令~")
        try:
            startTime = time.time()
            async with Client(
                item.info.host,
                item.info.rcon_port,
                item.info.rcon_password
            ) as c:
                ping, status = (time.time() - startTime) / 2, True
                other = f"Response: {((await c.send_cmd(cmd))[0])[0: 100]}"
        except:
            ping, status = -1, False
            other = "Error: Timeout"

        return await executeCmd.finish(
            createMsg(
                "服务器执行命令如下",
                item.info,
                status,
                ping,
                other
            )
        )

    return await executeCmd.finish("服务器不存在~")
