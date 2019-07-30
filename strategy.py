
import json

trade_buy_dict = {}
trade_sell_dict = {}

# 从文件中读历史数据
def read_from_file(file_name='2019-1.json'):
    with open(file=file_name, mode='r') as f:
        return json.load(f)

def strategy():
    history_list = read_from_file('2019-1.json')
    # {
    #     "vwap": 3691.9442,
    #     "close": 3693.0,
    #     "home_notional": 429.80036984,
    #     "trades": 463.0,
    #     "symbol": "XBTUSD",
    #     "open": 3689.0,
    #     "turnover": 42980036984.0,
    #     "last_size": 20.0,
    #     "high": 3693.5,
    #     "volume": 1586756.0,
    #     "timestamp": "2019-01-01 00:00",
    #     "foreign_notional": 1586756.0,
    #     "low": 3689.0
    # }
    for trad_dict in history_list:

        pass


if __name__ == '__main__':

    strategy()
    pass