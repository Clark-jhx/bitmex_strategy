import datetime
import swagger_client
from swagger_client import ApiClient
from swagger_client.rest import ApiException
import json
from swagger_client.models.trade_bin import TradeBin
import calendar


def test():
    lists = []
    times = get_times_2()
    list1 = get_trade_history(times[0])
    print(type(list1))
    lists += list1
    list2 = get_trade_history(times[1])
    lists += list2
    print(lists)
    write_to_file(lists)


# 一个月的数据
def one_month_history(year=2019, month=1):
    start_time = datetime.datetime(year, month, 1, 11, 59)
    end_time = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59)
    trades = []
    times = get_times()
    for time in times:
        if (start_time <= time) and (time < end_time):
            print(time)
            trade = get_trade_history(time=time, count=720)
            reversed_list = list(reversed(trade))
            trades += reversed_list
    file_name = '{}-{}.json'.format(start_time.year, start_time.month)
    write_to_file(trades, file_name=file_name)
    pass


# 所有历史数据写入文件，以月为单位
def history_to_file():
    times = get_times()
    trades = []
    year = times[0].year
    month = times[0].month
    for time in times:
        if (year != time.year) or (month != time.month):
            file_name = '{}-{}.json'.format(year, month)
            write_to_file(trades, file_name=file_name)
            print('生成文件 {}'.format(file_name))
            trades.clear()
        print(time)
        trade = get_trade_history(time=time, count=720)
        reversed_list = list(reversed(trade))
        trades += reversed_list
        year = time.year
        month = time.month


# 将列表写入文件
def write_to_file(lists, file_name='data.json'):
    # lists_str = '{history:' + lists.__str__() + '}'
    lists_str = lists.__str__()
    lists_str = lists_str.replace('\n', '').replace(" ", "").replace('\'', "\"")  # 去掉空格

    with open(file_name, 'w') as f:
        json.dump(lists, f, indent=4, cls=ComplexEncoder)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M')
        if isinstance(obj, swagger_client.models.trade_bin.TradeBin):
            # 转换成字典
            return obj.to_dict()
        else:
            print('未知类型', type(obj))
            return json.JSONEncoder.default(self, obj)


## 获取服务器时间列表
def get_times(start_year=2017, start_month=1, start_day=1, start_hour=11, start_minuter=59, delta_hour=12):
    start_time = datetime.datetime(start_year, start_month, start_day, start_hour, start_minuter, 0, 0)
    times = []
    var = 0
    end_time = datetime.datetime.now() - datetime.timedelta(days=1)
    while True:
        next_time = start_time + datetime.timedelta(hours=delta_hour * var)
        if next_time > end_time:
            return times
            break
        times.append(next_time)
        var += 1


## 处理服务器的时间差 8天8小时
def to_server_time(time):
    server_time = time - datetime.timedelta(days=8) - datetime.timedelta(hours=8)
    return server_time


def to_normal_time(time):
    normal_time = time + datetime.timedelta(days=8) + datetime.timedelta(hours=8)
    return normal_time


## 获取时间列表
def get_times_2(start_year=2019, start_month=7, start_day=20, start_hour=0, start_minuter=0, delta_hour=12):
    start_time = datetime.datetime(start_year, start_month, start_day, start_hour, start_minuter, 0, 0)
    times = [start_time.strftime('%Y-%m-%d %H:%M UTC+8:00')]
    var = 0
    end_time = datetime.datetime(2017, 1, 1, 0, 0, 0, 0)
    while True:
        var += 1
        next_time = start_time - datetime.timedelta(hours=delta_hour * var)
        if next_time < end_time:
            return times
            break
        times.append(next_time.strftime('%Y-%m-%d %H:%M UTC+8:00'))


## 参考https://www.bitmex.com/api/explorer/#!/Trade/Trade_getBucketed
def get_trade_history(time=None, count=4.0, symbol='XBTUSD', bin_size='1m'):
    api_client = ApiClient(header_name='Accept', header_value='application/json')
    api_client.configuration.host = 'https://www.bitmex.com/api/v1'
    api_instance = swagger_client.TradeApi(api_client=api_client)
    bin_size = '1m'  # str | Time interval to bucket by. Available options: [1m,5m,1h,1d]. (optional) (default to 1m)
    partial = False  # bool | If true, will send in-progress (incomplete) bins for the current time period. (optional) (default to false)
    symbol = symbol  # str | Instrument symbol. Send a bare series (e.g. XBU) to get data for the nearest expiring contract in that series.  You can also send a timeframe, e.g. `XBU:monthly`. Timeframes are `daily`, `weekly`, `monthly`, `quarterly`, and `biquarterly`. (optional)
    filter = ''  # str | Generic table filter. Send JSON key/value pairs, such as `{\"key\": \"value\"}`. You can key on individual fields, and do more advanced querying on timestamps. See the [Timestamp Docs](https://www.bitmex.com/app/restAPI#Timestamp-Filters) for more details. (optional)
    columns = ''  # str | Array of column names to fetch. If omitted, will return all columns.  Note that this method will always return item keys, even when not specified, so you may receive more columns that you expect. (optional)
    count = count  # float | Number of results to fetch. (optional) (default to 100)
    start = 0.0  # float | Starting point for results. (optional) (default to 0)
    reverse = False  # bool | If true, will sort results newest first. (optional) (default to false)
    server_time = to_server_time(time).strftime('%Y-%m-%d %H:%M')
    start_time = server_time  # datetime | Starting date filter for results. (optional)
    end_time = ''  # datetime | Ending date filter for results. (optional)

    try:
        # Get previous trades in time buckets.
        api_response = api_instance.trade_get_bucketed(bin_size=bin_size, partial=partial, symbol=symbol,
                                                       columns=columns, count=count, start=start, reverse=reverse,
                                                       start_time=start_time)
    except ApiException as e:
        print("Exception when calling TradeApi->trade_get_bucketed: %s\n" % e)
    return api_response


if __name__ == '__main__':
    history_to_file()
    # one_month_history()
    # test()
