from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Message

from . import data_source
from .models import fund_impl

# Usage: #fund <fundid> <compareddate(y-m-d)>
fund = on_command("fund", rule=None, priority=5)


@fund.handle()
async def handle_fund(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).split()
    result = ""
    if len(args) == 0:
        await fund.finish("#fund <fundid> <compareddate(y-m-d)>")
    elif len(args) >= 3:
        result += "超过的参数会被忽略\n"
    result = result + await fund_impl.fund_impl(args)
    msg = Message(result)
    print(msg)
    await bot.send(event, msg, False)
