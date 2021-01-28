import datetime
from functools import wraps
from typing import Union, List, Dict

import httpx
from nonebot.log import logger

from fundbot import util
from .util import decode_fund_data, decode_fund_range_data, get_timestamp_from_dt


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


async def get_fund_data(fund_id: str) -> Union[Dict, str]:
    recent_time = util.get_random_dt()
    url = f"https://fundgz.1234567.com.cn/js/{fund_id}.js?rt={recent_time}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = decode_fund_data(r)
        if data:
            return data
        else:
            return "卧槽查不到啊"


async def get_fund_data_hist(fund_id: str, start_date: str, end_date: str) -> Union[Dict, str]:
    recent_time = util.get_random_dt()
    try:
        start_time = get_timestamp_from_dt(start_date)
        end_time = get_timestamp_from_dt(end_date)
    except:
        logger.error(f"Error date format: start_date<{start_date}> end_date<{end_date}>")
        return "时间格式不对啊"
    if start_time > end_time or recent_time < end_time:
        return "你穿越回来得吗？"
    url = f"https://fundf10.eastmoney.com/F10DataApi.aspx?type=lsjz&code={fund_id}&page=1&per=1&sdate={start_date}&edate={end_date}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = decode_fund_range_data(r)
        if data:
            return data
        else:
            return "卧槽查不到啊"
