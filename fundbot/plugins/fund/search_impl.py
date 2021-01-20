import httpx
import time
import random
import asyncio

global data_list
data_list = None

global search_cache
search_cache = dict() # key: list, val: str

def get_random_dt():
    return int(time.time()*1000 - random.randint(1, 500))



async def get_all_fund():
    async with httpx.AsyncClient() as client:
        rand_rt = get_random_dt()
        url = f'https://fund.eastmoney.com/js/fundcode_search.js?dt={rand_rt}'
        r = await client.get(url)
        data = r.text
        data = eval(data[9:-1]) if 'var r = ' in data else None
        if data:
            return data
        else:
            return "出问题了，兄弟"

def cache_add(search_args: list, result: str) -> str:
    global search_cache
    # clear the cache if too large
    # maybe implement LRU in the future
    if len(search_cache) > 100:
        search_cache.clear()
    search_cache[search_args] = result
    


async def search_impl(args: str) -> str:
    global search_cache
    global data_list

    # search in the cache
    if args in search_cache.keys():
        return search_cache[args]

    # not in cache
    arg_list = args.split()
    if len(arg_list) == 0:
        return "用法: /search <arg1> ... <argn>"
    if not data_list:
        data_list = await get_all_fund()
    n_results = 0
    result = ""
    for item in data_list:
        code, name = item[0], item[2]
        valid = True
        for arg in arg_list:
            if name.find(arg) == -1:
                valid = False
                break
        if valid:
            result += f'{code}, {name}\n'
            n_results += 1
            if n_results >= 5:
                result += '仅返回前五条结果'
                break
    if result == "":
        result = "你在找锤子呢"
    cache_add(args, result)
    return result


async def test():
    while 1:
        x = input("input key words: ")
        res = await search_impl(x)
        print(res)

if __name__ == "__main__":
    asyncio.run(test())