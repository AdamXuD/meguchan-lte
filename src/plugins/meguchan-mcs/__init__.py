__usage__ = """
惠酱可以检测mc服务器的情况。
使用方法：
1. 发送 "/mc dels <服务器名称>" 可向惠酱删除服务器（仅指定的管理员可使用）。
2. 发送 "/mc check <服务器名称>" 可检测服务器状态。
3. 发送 "/mc list" 可查看本群或由您管理的服务器列表。
"""

__help_version__ = '1.0.0'

__help_plugin_name__ = "惠酱mc"


from html import unescape
import json

from mcstatus import MinecraftServer
from aiomcrcon import Client
import nonebot
from nonebot.plugin import require, on_regex
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, PrivateMessageEvent
from nonebot.params import RegexDict

from .config import ServerInfo, Config, appendServer, removeServer, serverList


scheduler = require("nonebot_plugin_apscheduler").scheduler
meguchan_config = Config.parse_obj(nonebot.get_driver().config.dict())


async def pingServer(host, queryPort):
    try:
        return await MinecraftServer(host, queryPort).async_ping(), True
    except:
        return None, False


@scheduler.scheduled_job("cron", minute="*/1", id="mcstatus")
async def _():
    try:
        bot = nonebot.get_bot()
    except:
        return

    for item in serverList:
        ping, status = await pingServer(item.info.host, item.info.query_port)

        if item.status == None:
            item.status = status
            continue
        if status != item.status:
            item.status = status
            groups = item.info.established_groups
            message = (
                "【服务器状态发生变化】\n"
                + f"Name: {item.info.name}\n"
                + f"Host: {item.info.host}\n"
                + f"Status: {'On' if status else 'Off'}\n"
                + f"Ping: {round(ping, 5)}ms" if status else ""
            )
            for group in groups:
                await bot.send_msg(
                    group_id=group,
                    message=message,
                )
            managers = [meguchan_config.meguchan_admin_id] + item.info.managers
            for manager in managers:
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
    if int(event.get_user_id()) != meguchan_config.meguchan_admin_id:
        return await addServer.finish("你不是惠酱管理员，不能添加服务器~")

    info = unescape(msg["info"])
    try:
        info = ServerInfo.parse_obj(json.loads(info))
        for item in serverList:
            if item.info.name == info.name:
                return await addServer.finish("服务器已存在~")

        ping, status = await pingServer(info.host, info.query_port)
        appendServer(info, status)
        message = (
            "【服务器添加成功】\n"
            + f"Name: {info.name}\n"
            + f"Host: {info.host}\n"
            + f"Status: {'On' if status else 'Off'}\n"
            + f"Ping: {round(ping, 5)}ms" if status else ""
        )
    except:
        message = "无效的服务器信息"
    return await addServer.finish(message)


deleteServer = on_regex("^/mc dels (?P<name>[a-zA-Z0-9]*)$")


@deleteServer.handle()
async def _(event: MessageEvent, msg: dict = RegexDict()):
    name = msg["name"]
    for item in serverList:
        if item.info.name == name:
            if int(event.get_user_id()) not in [meguchan_config.meguchan_admin_id] + item.info.managers:
                return await deleteServer.finish("你不是该服务器管理员，不能删除该服务器~")
            removeServer(item)
            return await deleteServer.finish("服务器删除成功~")
    return await deleteServer.finish("服务器不存在~")


checkStatus = on_regex("^/mc check (?P<name>[a-zA-Z0-9]*)$")


@checkStatus.handle()
async def _(msg: dict = RegexDict()):
    name = msg["name"]
    for item in serverList:
        if item.info.name == name:
            ping, status = await pingServer(item.info.host, item.info.query_port)
            if status:
                server = MinecraftServer(item.info.host, item.info.query_port)
                players = ", ".join(server.query().players.names)
                message = (
                    "【服务器状态如下】\n"
                    + f"Name: {item.info.name}\n"
                    + f"Host: {item.info.host}\n"
                    + f"Status: {'On' if status else 'Off'}\n"
                    + f"Ping: {round(ping, 5)}ms\n"
                    + f"Players: {players}\n"
                )
            else:
                message = (
                    "【服务器状态如下】\n"
                    + f"Name: {item.info.name}\n"
                    + f"Host: {item.info.host}\n"
                    + f"Status: {'On' if status else 'Off'}"
                )
            return await checkStatus.finish(message)
    return await checkStatus.finish("服务器不存在~")


listServer = on_regex("^/mc list$")


@listServer.handle()
async def _(event: MessageEvent):
    message = ("【订阅的服务器列表】\n")
    for item in serverList:
        if (isinstance(event, GroupMessageEvent) and event.group_id in item.info.established_groups) or\
                (isinstance(event, PrivateMessageEvent) and event.get_user_id() in item.info.managers + [meguchan_config.meguchan_admin_id]):
            message += (
                f"Name: {item.info.name}\n"
                + f"Host: {item.info.host}\n"
                + f"Status: {'On' if item.status else 'Off'}\n\n"
            )
    return await listServer.finish(message)


executeCmd = on_regex("^/mc exec (?P<name>[a-zA-Z0-9]*) `(?P<cmd>.*)`$")


@executeCmd.handle()
async def _(event: MessageEvent, msg: dict = RegexDict()):
    cmd = msg["cmd"]
    name = msg["name"]

    for item in serverList:
        if item.info.name == name:
            if int(event.get_user_id()) not in [meguchan_config.meguchan_admin_id] + item.info.managers:
                return await addServer.finish("您未被指定为该服务器管理员，不能使用命令~")
            async with Client(item.info.host, item.info.rcon_port, item.info.rcon_password) as c:
                resp = (await c.send_cmd(cmd))[0]
                return await executeCmd.finish(f"{name}: {resp if len(resp) < 100 else resp[0: 100] + '...'}")
    return await executeCmd.finish("服务器不存在~")
