import requests
import bs4
import pandas as pd

file_path = 'C:/Users/tianping/Desktop/symbol.csv'
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, li'
                  'ke Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
# Send a request to url.
html = requests.get(url, headers=headers).text
soup = bs4.BeautifulSoup(html, 'lxml')
table = soup.table
# Get every row of table.
table_l = table.find_all('tr')
# Get symbols.
symbol_l = []
for i in range(1, len(table_l)):
    symbol = table_l[i].find_all('a')[1].string
    symbol_l.append(symbol)
    print((i+1), ')', symbol)
# Write data into file.
pd.DataFrame(symbol_l).to_csv(file_path)





