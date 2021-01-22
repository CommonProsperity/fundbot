import random

from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Message

from . import search_impl

# Usage: #search <arg1> ... <argn>
search_cmd = on_command("search", rule=None, priority=5)


@search_cmd.handle()
async def handle_search(bot: Bot, event: Event, state: T_State):
    result = await search_impl.search_impl(str(event.get_message()))
    msg = Message(result)
    print(msg)
    await bot.send(event, msg, False)
