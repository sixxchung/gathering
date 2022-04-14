import urllib3
import pdb
import codecs
import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1~54
urllib3.disable_warnings()
HEADER = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

URL_main = 'https://www.topten10mall.com/kr/front/search/totalSearch.do'
urls = [
    f'{URL_main}?searchTerm=반팔티&currentPage={i}&rowsperPage=30&sort=saleCnt&searchType=total#none' for i in range(37)
]

goods = []
aPrice = []
bPrice = []
discount = []

for url in urls:
    response = requests.get(url, headers=HEADER, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    ProdNames = soup.find_all("p", attrs={"class": "card-goods__text"})
    ProdDetails = soup.find_all(
        "div", attrs={"class": "card-goods__priceInfo"})

    for i in range(30):  # i =5
        ProdName = ProdNames[i]
        ProdDetail = ProdDetails[i]
        afterPrice = ProdDetail.select_one("strong.card-goods__price")
        beforePrice = ProdDetail.find("s")
        percent = ProdDetail.select_one("strong.card-goods__discount")

        goods.append(ProdName.get_text() if ProdName != None else 'NoTitle')
        aPrice.append(afterPrice.get_text() if afterPrice != None else 0)
        bPrice.append(beforePrice.get_text() if beforePrice != None else 0)
        discount.append(percent.get_text() if percent != None else 0)


dresstable = pd.DataFrame({
    'goods':    goods,
    'aprice':  aPrice,
    'bprice':  bPrice,
    'discount': discount
})
dresstable.info()


def remove_symbol_to_int(x):
    x = str(x)
    x = x.replace(',', '')
    x = x.replace('%', '')
    x = int(x)
    return x


dresstable['goods'] = dresstable['goods'].apply(lambda x: str(x))
dresstable['bprice'] = dresstable['bprice'].apply(remove_symbol_to_int)
dresstable['aprice'] = dresstable['aprice'].apply(remove_symbol_to_int)
dresstable['discount'] = dresstable['discount'].apply(remove_symbol_to_int)
dresstable.info()

dresstable.to_parquet("myfile.parquet", engine='fastparquet')  # 23
dresstable.to_csv('mylife2.csv', index=False)                  # 85

df = dresstable


df = dresstable[dresstable.bprice > 30000].sort_values(
    'discount', ascending=False)

df = df.drop_duplicates(subset=None, keep='first',
                   inplace=False, ignore_index=False)

df.to_csv('df.csv', index=False)

df

dresstable = pd.DataFrame({
    'goods':    goods,
    'aprice':  aPrice,
    'bprice':  bPrice,
    'discount': discount
})

df.loc[[0,1,2]]  
df.loc[0:2]       #same
df.loc[0:2, :]    #same
df.loc[:, 0:2]    # x

df[[0,1,2,]]    # x
df[0:2]
df.iloc[[0,1]]  #same
df.iloc[0:2]    #same
df.iloc[0:2, :] #same

df.iloc[:, 0:2] # all row, slice column


