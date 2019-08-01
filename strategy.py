import json
from matplotlib import pyplot
import numpy


# 从文件中读历史数据
def read_from_file(file_name='2019-1.json'):
    with open(file=file_name, mode='r') as f:
        return json.load(f)


def picture(files=['2019-1.json'], use_quick_strategy=False):
    start_gap = int(0.5 * 100) # 涨跌0.5爆仓
    end_gap = int(5 * 100)
    delta = int(0.2 * 100)
    gaps = [x * 0.01 * 0.01 for x in range(start_gap, end_gap, delta)]

    gains = []
    double_burst = []
    loop_counts = []
    history_counts = []
    buy_counts = []
    sell_counts = []
    for gap in gaps:
        result_dict = special_month_strategy(files=files, gap=gap, gain=1, use_quick_strategy=use_quick_strategy)
        print(gap, result_dict)
        gain_count = result_dict['buy_count'] + result_dict['sell_count'] - result_dict['all_burst'] * 2
        gains.append(gain_count)
        double_burst.append(result_dict['all_burst'])
        loop_counts.append(result_dict['loop_count'])
        history_counts.append(result_dict['history_count'])
        buy_counts.append(result_dict['buy_count'])
        sell_counts.append(result_dict['sell_count'])

    # 图形输出
    print(gaps)
    print('历史k线数量', history_counts)
    print('交易次数', loop_counts)
    print('多头盈利次数', buy_counts)
    print('空头盈利次数', sell_counts)
    print('多空双爆', double_burst)
    print('获胜次数', gains)
    pyplot.plot([x * 100 for x in gaps], gains, 'o-g', linewidth=1, label='gain count')
    pyplot.plot([x * 100 for x in gaps], double_burst, 'o-r',  linewidth=1, label='double burst')
    pyplot.plot([x * 100 for x in gaps], loop_counts, 'o-b',  linewidth=1, label='loop count')
    pyplot.legend()
    pyplot.show()
    pass


def special_month_strategy(files=['2019-1.json'], gap=0.5 * 0.01, gain=1, use_quick_strategy=False):
    history_lists = []
    for file_name in files:
        history_list = read_from_file(file_name=file_name)
        history_lists += history_list
    if use_quick_strategy:
        return strategy_quick(history_list=history_lists, gap=gap, gain=gain)
    else:
        return strategy(history_list=history_lists, gap=gap, gain=gain)

def strategy_quick(history_list=[], gap=0.5 * 0.01, gain=1):
    loop_count = 0  # 交易循环次数
    buy_count = 0  # 多头盈利次数
    sell_count = 0  # 空头盈利次数
    all_burst = 0  # 多空双爆

    for index in range(0, len(history_list)-1, 10):
        trad_dict = history_list[index]
        close = trad_dict['close']
        open_buy_price = close # 多头 开仓价
        open_sell_price = close  # 空头 开仓价

        loop_count = loop_count + 1
        buy_end = False  # 多仓是否已平仓
        sell_end = False  # 空仓是否已平仓
        buy_burst_end = False  # 多头是否爆仓
        sell_burst_end = False  # 空头是否爆仓
        buy_gain_end = False  # 多投盈利平仓
        sell_gain_end = False  # 空头盈利平仓

        for index_ in range(index+1, len(history_list), 10):
            trad_dict_ = history_list[index_]
            high_ = trad_dict_['high']
            low_ = trad_dict_['low']
            if not buy_end:
                if high_ >= open_buy_price * (1 + gap * 2):
                    #print('{} >= {} 多头平仓'.format(high_, open_buy_price * (1 + gap + gap * gain)))
                    buy_end = True
                    buy_gain_end = True  # 多头盈利平仓
                if low_ <= open_buy_price * (1 - gap):
                    # print('{} >= {} 多头爆仓'.format(low_, open_buy_price * (1 - gap)))
                    buy_end = True
                    buy_burst_end = True  # 多头爆仓
            if not sell_end:
                if low_ <= open_sell_price * (1 - gap * 2):
                    #print('{} <= {} 空头平仓'.format(low_, open_sell_price * (1 - gap - gap * gain)))
                    sell_end = True
                    sell_gain_end = True  # 空头盈利平仓
                if high_ >= open_sell_price * (1 + gap):
                    # print('{} <= {} 空头爆仓'.format(high_, open_sell_price * (1 - gap)))
                    sell_end = True
                    sell_burst_end = True  # 空头爆仓

            if buy_end and sell_end:
                if buy_gain_end:
                    buy_count = buy_count + 1
                if sell_gain_end:
                    sell_count = sell_count + 1
                if buy_burst_end and sell_burst_end:
                    #print("双爆")
                    all_burst = all_burst + 1
                break

    result_dict = {}
    result_dict['loop_count'] = loop_count  # 交易次数
    result_dict['buy_count'] = buy_count  # 多头盈利次数
    result_dict['sell_count'] = sell_count  # 空头盈利次数
    result_dict['all_burst'] = all_burst  # 多空双爆
    result_dict['history_count'] = len(history_list) # 分钟线数量
    return result_dict

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
            if not buy_end:
                if high >= open_buy_price * (1 + gap * 2):
                    #print('{} >= {} 多头平仓'.format(high, open_buy_price * (1 + gap + gap * gain)))
                    buy_end = True
                    buy_gain_end = True  # 多头盈利平仓
                if low <= open_buy_price * (1 - gap):
                    #print('{} >= {} 多头爆仓'.format(low, open_buy_price * (1 - gap)))
                    buy_end = True
                    buy_burst_end = True  # 多头爆仓

            if not sell_end:
                if low <= open_sell_price * (1 - gap * 2):
                    #print('{} <= {} 空头平仓'.format(low, open_sell_price * (1 - gap - gap * gain)))
                    sell_end = True
                    sell_gain_end = True  # 空头盈利平仓
                if high >= open_sell_price * (1 + gap):
                    #print('{} <= {} 空头爆仓'.format(high, open_sell_price * (1 - gap)))
                    sell_end = True
                    sell_burst_end = True  # 空头爆仓

            if buy_end and sell_end:
                loop_end = True
                if buy_gain_end:
                    buy_count = buy_count + 1
                if sell_gain_end:
                    sell_count = sell_count + 1
                if buy_burst_end and sell_burst_end:
                    #print("双爆")
                    all_burst = all_burst + 1
    result_dict = {}
    result_dict['loop_count'] = loop_count # 交易次数
    result_dict['buy_count'] = buy_count # 多头盈利次数
    result_dict['sell_count'] = sell_count # 空头盈利次数
    result_dict['all_burst'] = all_burst # 多空双爆
    result_dict['history_count'] = len(history_list)  # 分钟线数量
    return result_dict

def test():
    gap = 3 * 0.01  # 爆仓百分比
    gain = 0.9  # 获利百分比
    files = []
    # files.append('2017-1.json')
    # files.append('2017-2.json')
    files.append('2017-3.json')
    result_dict = special_month_strategy(files=files, gap=gap, gain=gain)
    print(result_dict)

if __name__ == '__main__':
    files = []

    #files.append('2017-1.json')
    #files.append('2017-2.json')
    #files.append('2017-3.json')
    #files.append('2017-4.json')
    #files.append('2017-5.json')
    #files.append('2017-6.json')
    #files.append('2017-7.json')
    files.append('2018-7.json')

    picture(files=files, use_quick_strategy=True)
    pass
