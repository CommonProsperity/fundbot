#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot


# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init(_env_file=".env")
driver = nonebot.get_driver()
config = driver.config
config.command_start = set("!！/#")

nonebot.load_builtin_plugins()
app = nonebot.get_asgi()

driver.register_adapter("cqhttp", CQHTTPBot)


# nonebot.load_plugins("src/plugins")
nonebot.load_plugins("fundbot/plugins")

# Modify some config / config depends on loaded configs


if __name__ == "__main__":
    nonebot.run(app="bot:app")
