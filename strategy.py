import json

# 从文件中读历史数据
def read_from_file(file_name='2019-1.json'):
    with open(file=file_name, mode='r') as f:
        return json.load(f)

def picture():
    gaps = range(0.1 ,6 ,0.2)
    gains = []
    for gap in gaps:
        result_dict = special_month_strategy(files=['2019-1.json'], gap=gap, gain=1)
        gain_count = result_dict['buy_count'] + result_dict['sell_count'] - result_dict['all_burst'] * 2
        gains.append(gain_count)
    # todo 输入图形
    pyplot.plot(gaps, gains, '-r')
    pyplot.plot([1, 2, 3], [2, 4, 9], ':g')
    pyplot.show()
    pass


def special_month_strategy(files=[], gap=0.5 * 0.01, gain=1):
    history_lists = []
    for file_name in files:
        history_list = read_from_file(file_name=file_name)
        history_lists += history_list
    return strategy(history_list=history_lists, gap=gap, gain=gain)


def strategy(history_list=[], gap=0.5 * 0.01, gain=1):
    one = True
    loop_count = 0  # 交易循环次数
    buy_count = 0  # 多头盈利次数
    sell_count = 0  # 空头盈利次数
    all_burst = 0  # 多空双爆
    open_buy_price = history_list[0]['close']  # 多头 开仓价
    open_sell_price = history_list[0]['close']  # 空头 开仓价
    loop_end = False
    buy_end = False  # 多仓是否已平仓
    sell_end = False  # 空仓是否已平仓
    buy_burst_end = False  # 多头是否爆仓
    sell_burst_end = False  # 空头是否爆仓
    buy_gain_end = False  # 多投盈利平仓
    sell_gain_end = False  # 空头盈利平仓
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
        close = trad_dict['close']
        open = trad_dict['open']
        high = trad_dict['high']
        low = trad_dict['low']
        # 跳过第一次
        if one:
            one = False
            continue
        if loop_end:
            loop_count = loop_count + 1
            loop_end = False
            buy_end = False
            sell_end = False
            buy_gain_end = False
            buy_burst_end = False
            sell_gain_end = False
            sell_burst_end = False
            open_buy_price = close
            open_sell_price = close
            continue
        else:
            # print('多仓开价{} 空仓开价{} hight{} low{}'.format(open_buy_price, open_sell_price, high, low))
            # buy_high = abs(open_buy_price-high)/min(open_buy_price, high)
            # buy_low = abs(open_buy_price-low)/min(open_buy_price, low)
            # sell_high = abs(open_sell_price-high)/min(open_sell_price, high)
            # sell_low = abs(open_sell_price-low)/min(open_sell_price, low)
            # print(buy_high, buy_low, sell_high, sell_low)
            if not buy_end:
                if high >= open_buy_price * (1 + gap * 2):
                    print('{} >= {} 多头平仓'.format(high, open_buy_price * (1 + gap + gap * gain)))
                    buy_end = True
                    buy_gain_end = True  # 多头盈利平仓
                if low <= open_buy_price * (1 - gap):
                    print('{} >= {} 多头爆仓'.format(low, open_buy_price * (1 - gap)))
                    buy_end = True
                    buy_burst_end = True  # 多头爆仓

            if not sell_end:
                if low <= open_sell_price * (1 - gap * 2):
                    print('{} <= {} 空头平仓'.format(low, open_sell_price * (1 - gap - gap * gain)))
                    sell_end = True
                    sell_gain_end = True  # 空头盈利平仓
                if high >= open_sell_price * (1 + gap):
                    print('{} <= {} 空头爆仓'.format(high, open_sell_price * (1 - gap)))
                    sell_end = True
                    sell_burst_end = True  # 空头爆仓

            if buy_end and sell_end:
                loop_end = True
                if buy_gain_end:
                    buy_count = buy_count + 1
                if sell_gain_end:
                    sell_count = sell_count + 1
                if buy_burst_end and sell_burst_end:
                    all_burst = all_burst + 1
    result_dict = {}
    result_dict['loop_count'] = loop_count
    result_dict['buy_count'] = buy_count
    result_dict['sell_count'] = sell_count
    result_dict['all_burst'] = all_burst
    return result_dict


if __name__ == '__main__':
    gap = 3 * 0.01  # 爆仓百分比
    gain = 0.9  # 获利百分比
    files = []
    files.append('2019-1.json')
    result_dict = special_month_strategy(files=files, gap=gap, gain=gain)
    print('交易次数', result_dict['loop_count'])
    print('多头盈利次数', result_dict['buy_count'])
    print('空头盈利次数', result_dict['sell_count'])
    print('多空双爆', result_dict['all_burst'])
    print('最终盈利次数', result_dict['buy_count'] + result_dict['sell_count'] - result_dict['all_burst'] * 2)
    pass
