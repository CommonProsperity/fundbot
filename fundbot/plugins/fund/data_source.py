import time
import datetime
import random
from functools import wraps
import copy
from typing import Union, List, Dict

import httpx

from fundbot import util


def daily_cache(func):
    date = None
    cached = None

    @wraps(func)
    def _wrapper(*args, **kwargs):
        nonlocal date, cached
        cur_date = datetime.date.today()
        if date is None or cur_date > date:
            date = cur_date
            res = func(*args, **kwargs)
            cached = res
        return cached
    return _wrapper


# @daily_cache
async def get_all_fund() -> Union[List, str]:
    async with httpx.AsyncClient() as client:
        rand_rt = util.get_random_dt()
        url = f'https://fund.eastmoney.com/js/fundcode_search.js?dt={rand_rt}'
        r = await client.get(url)
        data = r.text
        data = eval(data[9:-1]) if 'var r = ' in data else None
        if data:
            return data
        else:
            return "出问题了，兄弟"


async def get_fund_data(fund_id: str) -> str:
    recent_time = util.get_random_dt()
    url = f"https://fundgz.1234567.com.cn/js/{fund_id}.js?rt={recent_time}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = decode_fund_data(r)
        if data:
            return format_fund_data(data)
        else:
            return "卧槽查不到啊"


def decode_fund_data(fund_data: str) -> Dict:
    data = fund_data.text
    if data[0:8] == 'jsonpgz(':
        return eval(data[8:-2])
    else:
        print("[ERROR] Not jsonpgz type")
        return None


def format_fund_data(fund_data: Dict) -> str:
    # format output
    result = ""
    format_pattern = "%s: %s\n"
    result += format_pattern % ("基金代号", fund_data["fundcode"])
    result += format_pattern % ("基金名称", fund_data["name"])
    result += "\n"
    result += format_pattern % ("单位净值", fund_data["dwjz"])
    result += format_pattern % ("日期", fund_data["jzrq"])
    result += format_pattern % ("估算净值", fund_data["gsz"])
    result += format_pattern % ("估算增值率", fund_data["gszzl"])
    result += format_pattern % ("估算时间", fund_data["gztime"])

    # delete last '\n'
    result = result[:-1]
    return result
