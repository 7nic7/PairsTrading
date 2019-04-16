from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import os
import time
# Define global variables
dir_path = 'C:\\Users\\tianping\\Downloads'
symbol_file = 'C:/Users/tianping/Desktop/symbol.csv'
url = 'http://db.resset.com/'
chrome_path = 'F:/Chrome/GoogleChrome_62.0.3202.62_PortableSoft/ChromePortable/App/Google Chrome/chromedriver.exe'
wait_gap = 3
user_name = 'statnankai'
pwd = 'statnankai'


def reach_download_page(driver):
    # Select 美股
    Select(driver.find_element_by_id('dbMsgId')).select_by_value('ResUSStk2015012604')
    # Select 行情 - 美股行情
    # Switch to menu frame
    driver.switch_to.frame('mainFrame')
    driver.switch_to.frame('menu')
    driver.find_element_by_id('jmenu2').click()
    driver.find_element_by_id('smenu9').click()
    # Switch to main frame
    driver.switch_to.parent_frame()
    driver.switch_to.frame('main')


def login():
    # Open a web-server.
    driver = webdriver.Chrome(chrome_path)
    driver.get(url)
    # login
    driver.find_element_by_name('loginName').send_keys(user_name)
    driver.find_element_by_name('loginPwd').send_keys(pwd)
    driver.find_element_by_xpath('/html/body/center/div[2]/div/form/img').click()
    return driver


def download_and_back(driver):
    # Input condition of search
    Select(driver.find_element_by_name('cSearchVar')).select_by_value('StkCd')
    driver.find_element_by_name('cSearchText').send_keys(symbol_one)
    # Select the file's format
    Select(driver.find_element_by_name('outputType')).select_by_value('csv')
    # Click '查询' button
    driver.find_element_by_name('search').click()
    # Click '下载到本地' button
    driver.find_element_by_name('ss').click()
    time.sleep(wait_gap)
    # Back to the last page
    driver.find_element_by_name('add').click()


def rename(i, symbol_one):
    # Get the newest file
    file_list = os.listdir(dir_path)
    file_list.sort(key=lambda fn: os.path.getmtime(dir_path + "\\" + fn))
    print('         The newest file is %s' % file_list[-1])
    # Rename the newest file by symbol's name
    old_name = file_list[-1]
    new_name = '%d_%s.csv' % (i, symbol_one)
    os.rename(os.path.join(dir_path, old_name), os.path.join(dir_path, new_name))
    print('         Rename the %s to %s' % (file_list[-1], new_name))

if __name__ == '__main__':
    # Login
    driver = login()
    # Reach the download page
    reach_download_page(driver)
    # Read symbol.csv
    symbol = pd.read_csv(symbol_file, index_col=0)
    failure = []
    for i in range(464, len(symbol)):
        symbol_one = symbol.ix[i, 0]
        print('--- Ready to get the price of %s' % symbol_one)
        try:
            # Download file
            download_and_back(driver)
            print('         Download is done!')
            # Rename file
            rename(i, symbol_one)
        except:
            failure.append(symbol_one)
            print('         Download is failed!')
            # Refresh the page
            driver.refresh()
            reach_download_page(driver)

    if failure:
        print(failure)
