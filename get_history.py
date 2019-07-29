from __future__ import print_function
import swagger_client
from pprint import pprint
from swagger_client import ApiClient
from swagger_client.rest import ApiException


def get_trade():
    api_client = ApiClient()
    api_client.configuration.host = 'https://www.bitmex.com/api/v1'
    # create an instance of the API class
    api_instance = swagger_client.TradeApi(api_client=api_client)
    bin_size = '1m'  # str | Time interval to bucket by. Available options: [1m,5m,1h,1d]. (optional) (default to 1m)
    partial = False  # bool | If true, will send in-progress (incomplete) bins for the current time period. (optional) (default to false)
    symbol = 'XBTUSD'  # str | Instrument symbol. Send a bare series (e.g. XBU) to get data for the nearest expiring contract in that series.  You can also send a timeframe, e.g. `XBU:monthly`. Timeframes are `daily`, `weekly`, `monthly`, `quarterly`, and `biquarterly`. (optional)
    filter = ''  # str | Generic table filter. Send JSON key/value pairs, such as `{\"key\": \"value\"}`. You can key on individual fields, and do more advanced querying on timestamps. See the [Timestamp Docs](https://www.bitmex.com/app/restAPI#Timestamp-Filters) for more details. (optional)
    columns = ''  # str | Array of column names to fetch. If omitted, will return all columns.  Note that this method will always return item keys, even when not specified, so you may receive more columns that you expect. (optional)
    count = 3  # float | Number of results to fetch. (optional) (default to 100)
    start = 0  # float | Starting point for results. (optional) (default to 0)
    reverse = False  # bool | If true, will sort results newest first. (optional) (default to false)
    start_time = '2016-12-24 00:00 UTC+0:00'  # datetime | Starting date filter for results. (optional)
    end_time = ''  # datetime | Ending date filter for results. (optional)

    try:
        # Get previous trades in time buckets.
        api_response = api_instance.trade_get_bucketed(bin_size=bin_size, partial=partial, symbol=symbol, filter=filter,
                                                       columns=columns, count=count, start=start, reverse=reverse,
                                                       start_time=start_time, end_time=end_time)
        for a in api_response:
            print(a)
        #pprint(api_response)
    except ApiException as e:
        print("Exception when calling TradeApi->trade_get_bucketed: %s\n" % e)


if __name__ == '__main__':
    get_trade()
    pass
