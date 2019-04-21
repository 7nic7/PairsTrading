import os
import pandas as pd
from PairsTrading.config import Config
from talib import abstract
import numpy as np
# Define global variables
dir_path = 'G:/python_file/PairsTrading/'


# You can change the column's name of data.
def get_one_file_close(stock_file):
    """Read data from a stock file and create a data frame for (close price - open price)"""
    stock_name = stock_file[:-4]
    data = pd.read_csv(os.path.join(dir_path, 'data/S&P500/%s' % stock_file),
                       index_col='截止日期_EndDt',
                       encoding='ANSI')
    close_price = pd.DataFrame(data['收盘价_ClPr'].tolist(),
                               index=data.index,
                               columns=[stock_name])
    return close_price


def get_stock(file='result/adfuller.csv'):
    """Get stock names of which p_value of adfuller test is larger than 0.05"""
    adfuller = pd.read_csv(os.path.join(dir_path, file), index_col=0)
    p_values = adfuller['p-value'].fillna(0)
    symbols = adfuller.ix[p_values > 0.05, '股票代码'].tolist()
    index = adfuller.index[p_values > 0.05].tolist()
    file_names = [str(i)+'_'+j for i, j in zip(index, symbols)]
    return file_names


def normalize(data):
    """Normalization."""
    return (data - data[0]) / data[0]


def split_x_y(data, train_len):
    """Split data into x and y"""
    x, y = [], []
    for i in range(data.shape[0]-train_len):
        x_y = data[i:(i+train_len+1)]
        # Normalization
        x_y_norm = normalize(x_y)
        x.append(x_y_norm[:-1])
        y.append(x_y_norm[-1])
    # Transform the data type
    x, y = np.array(x), np.array(y)
    return x, y


def split_data(stock_name, fromdate=None, todate=None, train_len=60):
    """Split data from one stock file into training data and testing data."""
    data = pd.read_csv(os.path.join(dir_path, 'data/S&P500/%s.csv' % stock_name),
                       index_col='截止日期_EndDt',
                       encoding='ANSI')
    # Fill the NA with the previous number
    data = data.fillna(method='pad')
    var_name = ['开盘价_OpPr', '最高价_HiPr', '最低价_LoPr', '收盘价_ClPr', '成交量_TrdVol']
    # Get training set and testing set
    training_data = np.array(data.ix[fromdate:todate, var_name])
    testing_data = np.array(data.ix[todate:, var_name])
    # Get x_train, y_train, x_test, y_test
    x_train, y_train = split_x_y(training_data, train_len)
    x_test, y_test = split_x_y(testing_data, train_len)
    return x_train, y_train, x_test, y_test, testing_data


def get_input_arrays(row):
    """Create input arrays for talib's functions."""
    inputs = {
        'open': row[:, 0],
        'high': row[:, 1],
        'low': row[:, 2],
        'close': row[:, 3],
        'volume': row[:, 4],
    }
    return inputs


def get_other_vars(x_train, x_test):
    """Create x of which rows indicate variable's name and columns indicate sample's name."""
    # Read config file
    config = Config()
    indicators = config.indicators
    origin_x = np.concatenate([x_train, x_test], axis=0)
    x = []
    rownames = [k+'.lag'+str(i) for k in config.indicators.keys() for i in range(config.lag, 0, -1)]
    # Read stocks which are not stable on time series
    for row in origin_x:
        inputs = get_input_arrays(row)      # shape: 60*5
        sample = []
        # Calculate the indicators' values of one row
        for key in indicators:
            params = indicators[key]
            if '.' in key:
                key = key[:key.find('.')]
            func = abstract.Function(key)
            outputs = func(inputs, **params)
            # Add the outputs into sample list
            sample.extend(outputs[(-config.lag):].tolist())
        x.append(sample)
    # Transform the x's type
    x = np.array(x)
    var_train, var_test = x[:x_train.shape[0]], x[x_train.shape[0]:]
    return var_train, var_test, rownames


# main
def get_stock_x_y(stock_name, fromdate=None, todate=None, train_len=60):
    """Get x data and y data of one stock."""
    x_train, y_train, x_test, y_test, y_test_base = split_data(stock_name,
                                                               fromdate=fromdate,
                                                               todate=todate,
                                                               train_len=train_len)
    var_train, var_test, rownames = get_other_vars(x_train, x_test)
    # Build x_train and x_test by all of the variables
    x_train = np.concatenate([x_train.reshape([-1, train_len*5]), var_train], axis=1)
    x_test = np.concatenate([x_test.reshape([-1, train_len*5]), var_test], axis=1)
    print(x_train.shape)
    print(x_test.shape)
    print(x_test[0])


if __name__ == '__main__':
    # i = get_input_arrays(get_stock()[0], '2000-02-01', '2000-03-08 ')
    # print(i)
    # a = get_x('2000-02-01', '2001-03-08 ')
    # print(a)
    # x_tr, y_tr, x_te, y_te, y_te_base = split_data('0_MMM',
    #                                                fromdate='2000-02-01',
    #                                                todate='2012-02-01',
    #                                                train_len=60)
    # print(x_tr.shape)
    # print(y_tr.shape)
    get_stock_x_y('0_MMM', fromdate='2000-02-01', todate='2012-02-01', train_len=60)
