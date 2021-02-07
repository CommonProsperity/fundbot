from .. import data_source
from ..util import format_fund_data
from typing import Dict

async def fund_impl(args: list) -> str:
    # get fund data with fund_id
    raw_data = await data_source.get_fund_data(args[0])
    if type(raw_data) is str:
        return raw_data
    # case: <compareddate(y-m-d)> in param
    compared_data = None
    if len(args) == 2:
        compared_data = await data_source.get_fund_data_hist(args[0], args[1], args[1], 1, 1)
        if type(compared_data) is str:
            return compared_data
        elif type(compared_data) is Dict and len(compared_data.get("fund_data", [])) != 1:
            return "出问题了，兄弟"
    return format_fund_data(fund_data=raw_data, compared_data=compared_data.get("fund_data")[0])
