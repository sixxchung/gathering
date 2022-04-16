import urllib3
import requests
from bs4 import BeautifulSoup
import pandas as pd

import pdb
import codecs
import sys

# 1~54
Search_word = '반팔티'
urllib3.disable_warnings()
HEADER = {"user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
URL_main = 'https://www.topten10mall.com/kr/front/search/totalSearch.do'


goods = []
aPrice = []
bPrice = []
discount = []
# url = urls[6]
#for url in urls:
page = 0
while True:
    print(page)
    page = page + 1
    url = f'{URL_main}?searchTerm={Search_word}&currentPage={page}&rowsperPage=30&sort=saleCnt&searchType=total#none'
    
    response = requests.get(url, headers=HEADER, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    xx = soup.find("p", attrs={"class": "d-flex justify-content-center text-medium text-bold margin-b-12"})
    if xx != None :
        break
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
#dresstable.info()


def remove_symbol_to_int(x):
    x = str(x)
    x = x.replace(',', '')
    x = x.replace('%', '')
    x = int(x)
    return x


dresstable['goods']    = dresstable['goods'].apply(lambda x: str(x))
dresstable['bprice']   = dresstable['bprice'].apply(remove_symbol_to_int)
dresstable['aprice']   = dresstable['aprice'].apply(remove_symbol_to_int)
dresstable['discount'] = dresstable['discount'].apply(remove_symbol_to_int)
#dresstable.info()

# dresstable.to_parquet("myfile.parquet", engine='fastparquet')  # 23
# dresstable.to_csv('mylife2.csv', index=False)                  # 85

df = dresstable
df.info()

# ----------------------------------------------------------

df = df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
df = df.loc[df.bprice > 40000]
df = df.loc[df.aprice < 30000]
df = df.loc[-df.goods.str.contains('카라')]
df = df.sort_values('discount', ascending=False)

df.to_csv('df.csv', index=False)

goodsNm = df.goods[0]
https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=

dresstable = pd.DataFrame({
    'goods':    goods,
    'aprice':  aPrice,
    'bprice':  bPrice,
    'discount': discount
})




