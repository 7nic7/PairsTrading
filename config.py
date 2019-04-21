"""
    Config file:
        You can choose variables here.The details of the indicators are in following web.
        "https://github.com/HuaRongSAO/talib-document/blob/master/func_groups"
        Params:
            - indicators:
                Dict. You can define it like this {func_name: params}.And the 'params' is
                also a dict.If the indicator is the same but is different in timeperiod, you
                can define it like this {func_name.timeperiod: params}.
            - lag:
                Int. That's how many days ago to predict the response variables.
"""
# 还没处理多输出问题，不知道这些变量要不要加入到 X 中
indicators = {
    # 'STOCH': {'fastk_period': 5,
    #           'slowk_period': 3,
    #           'slowk_matype': 0,
    #           'slowd_period': 3,
    #           'slowd_matype': 0},
    'MA.30': {'timeperiod': 30},
    'MA.100': {'timeperiod': 100},
    'CCI.14': {'timeperiod': 14},
    'CCI.100': {'timeperiod': 100},
    'RSI.14': {'timeperiod': 14},
    'RSI.100': {'timeperiod': 100},
    'WILLR.14': {'timeperiod': 14},
    'WILLR.50': {'timeperiod': 50},
    'MOM.10': {'timeperiod': 10},
    'MOM.100': {'timeperiod': 100},
    # 'MACD': {'fastperiod': 12,
    #          'slowperiod': 26,
    #          'signalperiod': 9},
    'ROC.10': {'timeperiod': 10},
    'ROC.100': {'timeperiod': 100},
}

lag = 3


class Config:
    def __init__(self, indicators=indicators, lag=lag):
        self.indicators = indicators
        self.lag = lag