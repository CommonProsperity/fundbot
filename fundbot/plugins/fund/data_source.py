import httpx
import requests
import time
import random

async def getFundData(fund_id):
    fund_id = str(fund_id)
    recent_time = time.time()*1000 - random.randint(1,500)
    recent_time = str(int(recent_time))
    url = "http://fundgz.1234567.com.cn/js/%s.js?rt=%s" % (fund_id, recent_time)
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = decodeFundData(r)
        if data:
            return scanfFundJson(data)
        else:
            return "请输入正确的基金代号"

def decodeFundData(fund_data):
    data = fund_data.text
    if data[0:8] == 'jsonpgz(':
        return eval(data[8:-2])
    else:
        print("[ERROR] Not jsonpgz type")
        return None

def scanfFundJson(json_file):
    # format output
    result = ""
    format_pattern = "%s: %s\n"
    result += format_pattern % ("基金代号", json_file["fundcode"])
    result += format_pattern % ("基金名称", json_file["name"])
    # result += "\n"
    # result += format_pattern % ("单位净值", json_file["dwjz"])
    # result += format_pattern % ("日期", json_file["jzrq"])
    result += "\n"
    # result += format_pattern % ("估算净值", json_file["gsz"])
    result += format_pattern % ("估算增值率", json_file["gszzl"])
    result += format_pattern % ("估算时间", json_file["gztime"])

    # delete last '\n'
    result = result[:-1]
    return result
    
