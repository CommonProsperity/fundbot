import random

from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Message

from . import data_source
from .util import format_fund_data

# Usage: #fund <fundid>
fund = on_command("randfund", rule=None, priority=5)


@fund.handle()
async def handle_fund(bot: Bot, event: Event, state: T_State):
    result = await data_source.get_all_fund()
    if type(result) is str:
        fund_data = result
    else:
        fund_id, *_ = random.choice(result)
        raw_data = await data_source.get_fund_data(fund_id)
        if type(raw_data) is str:
            fund_data = raw_data
        else:
            fund_data = format_fund_data(raw_data)
    msg = Message(fund_data)
    print(msg)
    await bot.send(event, msg, False)
