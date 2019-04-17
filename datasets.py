import os
import pandas as pd


# You can change the column's name of data.
def get_one_file_output(stock_file, dir_path='G:/python_file/PairsTrading/data/'):
    """Read data from a stock file and create a data frame for (close price - open price)"""
    stock_name = stock_file[:-4]
    data = pd.read_csv(os.path.join(dir_path, 'S&P500/%s' % stock_file),
                       index_col='截止日期_EndDt',
                       encoding='ANSI')
    output = pd.DataFrame(data['收盘价_ClPr'].tolist(),
                          index=data.index,
                          columns=[stock_name])
    return output
