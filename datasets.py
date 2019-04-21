import os
import pandas as pd
from PairsTrading.config import Config
from talib import abstract
# Define global variables
dir_path = 'G:/python_file/PairsTrading/'


# You can change the column's name of data.
def get_one_file_close(stock_file, dir_path=dir_path):
    """Read data from a stock file and create a data frame for (close price - open price)"""
    stock_name = stock_file[:-4]
    data = pd.read_csv(os.path.join(dir_path, 'data/S&P500/%s' % stock_file),
                       index_col='截止日期_EndDt',
                       encoding='ANSI')
    close_price = pd.DataFrame(data['收盘价_ClPr'].tolist(),
                               index=data.index,
                               columns=[stock_name])
    return close_price


def get_stock(file='result/adfuller.csv', dir_path=dir_path):
    """Get stock names of which p_value of adfuller test is larger than 0.05"""
    adfuller = pd.read_csv(os.path.join(dir_path, file), index_col=0)
    p_values = adfuller['p-value'].fillna(0)
    symbols = adfuller.ix[p_values > 0.05, '股票代码'].tolist()
    index = adfuller.index[p_values > 0.05].tolist()
    file_names = [str(i)+'_'+j for i, j in zip(index, symbols)]
    return file_names


def get_input_arrays(stock_name, fromdate=None, todate=None, dir_path=dir_path):
    """Create input arrays for talib's functions."""
    data = pd.read_csv(os.path.join(dir_path, 'data/S&P500/%s.csv' % stock_name),
                       index_col='截止日期_EndDt',
                       encoding='ANSI')
    var_name = ['开盘价_OpPr', '最高价_HiPr', '最低价_LoPr', '收盘价_ClPr', '成交量_TrdVol']
    var_data = data.ix[fromdate:todate, var_name]
    inputs = {
        'open': var_data['开盘价_OpPr'].values,
        'high': var_data['最高价_HiPr'].values,
        'low': var_data['最低价_LoPr'].values,
        'close': var_data['收盘价_ClPr'].values,
        'volume': var_data['成交量_TrdVol'].values
    }
    return inputs


def get_x(fromdate, todate):
    """Create x of which rows indicate variable's name and columns indicate sample's name."""
    # Read config file
    config = Config()
    indicators = config.indicators
    stock_li = get_stock()
    x = {}
    rownames = [k+'.lag'+str(i) for k in config.indicators.keys() for i in range(config.lag, 0, -1)]
    # Read stocks which are not stable on time series
    for stock in stock_li:
        inputs = get_input_arrays(stock, fromdate, todate)
        sample = []
        # Calculate the indicators' values of one sample
        for key in indicators:
            params = indicators[key]
            if '.' in key:
                key = key[:key.find('.')]
            func = abstract.Function(key)
            outputs = func(inputs, **params)
            # Add the outputs into sample list
            sample.extend(outputs[(-config.lag):].tolist())
        x[stock] = sample
    out = pd.DataFrame(x, index=rownames)
    return out


if __name__ == '__main__':
    # i = get_input_arrays(get_stock()[0], '2000-02-01', '2000-03-08 ')
    # print(i)
    a = get_x('2000-02-01', '2001-03-08 ')
    print(a)
