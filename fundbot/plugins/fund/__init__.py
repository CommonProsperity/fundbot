import nonebot
from .config import Config

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from . import data_source

# Usage: #fund <fundid>
fund = on_command("fund", rule=None, priority=5)

@fund.handle()
async def handle_fund(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    result = ""
    if len(args)==0:
        await fund.finish("用法: #fund <fundid>")
    elif len(args)>=2:
        result += "超过的参数会被忽略\n"
    result = result + (await data_source.getFundData(args[0]))
    await fund.finish(result)

