__usage__ = """
惠酱可以缝合两个emoji。
使用方法：
发送任意两个即可。
"""

__help_version__ = '1.0.0'

__help_plugin_name__ = "惠酱pixiv"

from nonebot import on_regex
from nonebot.params import RegexDict
from nonebot.adapters.onebot.v11 import MessageSegment, Event
import emoji as emojilib

from .data_source import mix_emoji

pattern = emojilib.get_emoji_regexp().pattern
emojimix = on_regex(
    rf"(.*)?(?P<code1>{pattern})(?P<code2>{pattern})(.*)?", block=True, priority=13
)


@emojimix.handle()
async def _(msg: dict = RegexDict()):
    emoji_code1 = msg["code1"]
    emoji_code2 = msg["code2"]
    result = await mix_emoji(emoji_code1, emoji_code2)
    if isinstance(result, str):
        await emojimix.finish(result)
    else:
        await emojimix.finish(MessageSegment.image(result))
