import nonebot
from .config import Config
from . import fund

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
