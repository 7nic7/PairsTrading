from PairsTrading.datasets import get_one_file_output

from statsmodels.tsa.stattools import adfuller
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# Define global variables
dir_path = 'G:/python_file/PairsTrading/'

plt.ion()
fig, ax = plt.subplots(1, 1)
p_value_l, len_l, names_l, stat_l, confit_l = [], [], [], [], []
file_lists = os.listdir(os.path.join(dir_path, 'data/S&P500'))       # For example: '0_MMM.csv'
# Sort the files by download time
file_lists.sort(key=lambda fn: os.path.getmtime(dir_path+'data/S&P500/'+fn))
for index, file in enumerate(file_lists):
    # Get one file's close price
    close = get_one_file_output(file)
    name = file[(file.find('_')+1):-4]
    length = close.shape[0]
    names_l.append(name)
    len_l.append(length)
    # Filter the time length of stock less than 3990
    if length < 3990:
        p_value_l.append(np.nan)
        stat_l.append(np.nan)
        confit_l.append(np.nan)
        continue
    close = close.fillna(method='pad')
    close = np.array(close)
    # Interactive plot
    ax.clear()
    ax.plot(close)
    plt.title(name); plt.draw(); plt.pause(0.1)
    # Adf Test
    result = adfuller(close.T.squeeze())
    p_value_l.append(result[1])
    stat_l.append(result[0])
    confit_l.append(result[4])
    print('%d) %s p value : %.5f' % (index, name, result[1]))

plt.ioff()
# Write the result to file
data = {'股票代码': names_l,
        'p-value': p_value_l,
        '时间长度': len_l,
        'adf统计量': stat_l,
        '置信': confit_l}
pd.DataFrame(data).to_csv(os.path.join(dir_path, 'result/adfuller.csv'))
