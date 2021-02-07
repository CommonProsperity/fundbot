import time
import traceback
from typing import Dict
from nonebot.log import logger
from bs4 import BeautifulSoup


def get_timestamp_from_dt(date):
    try:
        time_array = time.strptime(date, "%Y-%m-%d")
        time_stamp = int(time.mktime(time_array)*1000)
    except Exception as e:
        raise e
    return time_stamp


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
        if raw_data[0:22] == 'var apidata={ content:' and raw_data.find("records:") != -1:
            fund_info = raw_data[23:raw_data.find("records:")-2]
            page_info = raw_data[raw_data.find("records:"):-2]
        else:
            logger.error("Not jsonpgz type")
            return None
        fund_data = []
        soup = BeautifulSoup(fund_info, 'html')
        entries_len = len(soup.table.tbody.select('tr'))
        for i in range(entries_len):
            entry_html = soup.table.tbody.select('tr')[i]
            if len(entry_html.select('td')) == 7:
                entry_data = {}
                entry_data["jzrq"] = entry_html.select('td')[0].text
                entry_data["gsz"] = entry_html.select('td')[1].text
                fund_data.append(entry_data)
        return {"fund_data": fund_data, "page_info": page_info}
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
    # calculate grouth rate if compared data is not empty
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

def format_fund_hist_data(fund_hist_data: Dict, fund_id: str = "") -> str:
    # format output
    result = ""
    if fund_id:
        result += f"基金代号: {fund_id}\n"
    format_pattern = "%s: %s; %s: %s\n"
    for fund_data in fund_hist_data["fund_data"]:
        result += format_pattern % ("日期", fund_data["jzrq"], "单位净值", fund_data["gsz"])
    result += f"<{fund_hist_data['page_info']}>"
    return result
