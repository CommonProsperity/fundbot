from .. import data_source
from ..util import format_fund_data


async def fund_impl(args: list) -> str:
    # get fund data with fund_id
    raw_data = await data_source.get_fund_data(args[0])
    if type(raw_data) is str:
        return raw_data
    # case: <compareddate(y-m-d)> in param
    compared_data = None
    if len(args) == 2:
        compared_data = await data_source.get_fund_data_hist(args[0], args[1], args[1])
        if type(compared_data) is str:
            return compared_data
    return format_fund_data(fund_data=raw_data, compared_data=compared_data)
