from . import data_source
from datetime import date
import math


data_list = None
search_cache = dict()  # key: list, val: str
cached_date = None

ITEMS_PER_PAGE = 5
_USAGE = f"""用法: /search <arg1> ... <argn> [page]
show {ITEMS_PER_PAGE} per page, and page ∈ N+
"""


def cache_add(search_args: list, result: str) -> str:
    global search_cache
    # clear the cache if too large
    # maybe implement LRU in the future
    if len(search_cache) > 100:
        search_cache.clear()
    search_cache[search_args] = result


async def search_impl(args: str) -> str:
    global search_cache, data_list, cached_date

    # search in the cache
    if args in search_cache.keys():
        return search_cache[args]

    # not in cache
    arg_list = args.split()
    if len(arg_list) == 0:
        return _USAGE
    cur_date = date.today()
    if not data_list or cached_date is None or cur_date != cached_date:
        data_list = await data_source.get_all_fund()
        cached_date = cur_date
    try:
        page = int(arg_list[-1]) - 1
        arg_list = arg_list[:-1]
    except:
        page = 0
    if page < 0:
        return _USAGE
    search_result = [i for i in data_list if all(x in i[2] for x in arg_list)]
    start = page * ITEMS_PER_PAGE
    end = min(start + ITEMS_PER_PAGE, len(search_result))
    if start >= end:
        return "你在找锤子呢"
    result = '\n'.join(f'{i[0]}, {i[2]}' for i in search_result[start:end])
    result += f'\n{page + 1}/{math.ceil(len(search_result)/ITEMS_PER_PAGE)}'
    return result
