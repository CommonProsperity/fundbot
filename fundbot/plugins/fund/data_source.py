import datetime
from functools import wraps
from typing import Union, List, Dict
import traceback
import asyncio

import httpx
from nonebot.log import logger, default_format
from bs4 import BeautifulSoup

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


async def make_request(client, url):
    r = await client.get(url)
    return r


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


async def get_fund_trend_data(fund_id: str, start_date: str) ->  str:
    recent_time = util.get_random_dt()
    try:
        start_time = util.get_timestamp_from_dt(start_date)
    except ValueError:
        logger.error(f"Error date format: {start_date}")
        return "时间格式不对啊"
    except:
        traceback.print_exc()
        logger.error(f"Date format: {start_date}")
    if start_time >= recent_time:
        return "你穿越回来得吗？"
    start_date_url = f"https://fundf10.eastmoney.com/F10DataApi.aspx?type=lsjz&code={fund_id}&page=1&per=1&sdate={start_date}&edate={start_date}"
    recent_date_url = f"https://fundgz.1234567.com.cn/js/{fund_id}.js?rt={recent_time}"
    async with httpx.AsyncClient() as client:
        task_list = []
        recent_date_req = make_request(client, recent_date_url)
        recent_date_task = asyncio.create_task(recent_date_req)
        task_list.append(recent_date_task)
        start_date_req = make_request(client, start_date_url)
        start_date_task = asyncio.create_task(start_date_req)
        task_list.append(start_date_task)
        r = await asyncio.gather(*task_list)
    if len(r) == 2 and r[0] and r[1]:
        recent_data = decode_fund_data(r[0])
        start_data = decode_fund_range_data(r[1])
        return format_fund_data(fund_data=recent_data, compared_data=start_data)
    else:
        return "出问题了，兄弟"


def decode_fund_data(fund_data: str) -> Dict:
    data = fund_data.text
    try:
        if data[0:8] == 'jsonpgz(':
            return eval(data[8:-2])
        else:
            logger.error("Not jsonpgz type")
            return None
    except:
        traceback.print_exc()
        logger.error(data)


def decode_fund_range_data(fund_range_data: str) -> Dict:
    raw_data = fund_range_data.text
    try:
        if raw_data[0:22] == 'var apidata={ content:':
            raw_data = raw_data[23:raw_data.find("records:")-2]
        else:
            logger.error("Not jsonpgz type")
            return None
        fund_data = {}
        soup = BeautifulSoup(raw_data, 'html')
        if len(soup.table.tbody.tr.select('td')) < 7:
            return {"jzrq":"", "gsz":""}
        fund_data["jzrq"] = soup.table.tbody.tr.select('td')[0].text
        fund_data["gsz"] = soup.table.tbody.tr.select('td')[1].text
        return fund_data
    except:
        traceback.print_exc()
        logger.error(raw_data)


def format_fund_data(fund_data: Dict, compared_data: Dict = None) -> str:
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
    if compared_data:
        if not compared_data['jzrq'] or not compared_data['gsz']:
            result += f"\n\n指定日期非交易日或数据已过期"
        else:
            result += format_pattern % (f"净值对比{compared_data['jzrq']}增长", format(float(fund_data["gsz"]) - float(compared_data["gsz"]), '.4f'))
    # delete last '\n'
    result = result[:-1]
    if float(fund_data['gszzl']) < 0:
        result += '\n\n这谁的\U0001F414，太垃圾了吧？'
    return result
