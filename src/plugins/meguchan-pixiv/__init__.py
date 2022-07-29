__usage__ = """
惠酱可以查询对应pid的Pixiv图片。
使用方法：
发送 "惠酱p站 <pid>" 可向惠酱查询对应pid的Pixiv图片（无需代理）。
"""

__help_version__ = '1.0.0'

__help_plugin_name__ = "惠酱pixiv"

from nonebot import get_driver
from nonebot.plugin import on_regex
from nonebot.params import RegexDict

from .config import Config


pixiv = on_regex("^惠酱[pP]站(\s)?(?P<pid>\d+)", priority=2)

meguchan_config = Config.parse_obj(get_driver().config.dict())


@pixiv.handle()
async def _(msg: dict = RegexDict()):
    pid = msg["pid"]
    await pixiv.send(f"{meguchan_config.meguchan_url}/pixiv/{pid}")
    await pixiv.finish("搜索完成~")
