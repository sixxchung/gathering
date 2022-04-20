import urllib3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pdb
import codecs
import sys

# 1~54
Search_word = '반팔티'
v_url = "https://www.topten10mall.com"
v_url_main = f'{v_url}/kr/front/search/totalSearch.do'
urllib3.disable_warnings()
HEADER = {"user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

def remove_others_to_str(x):
    x = str(x)
    x = x.replace('\n', '')
    x = x.strip()
    return x

def remove_symbol_to_int(x):
    x = str(x)
    x = x.replace(',', '')
    x = x.replace('%', '')
    x = x.replace('원', '')
    x = int(x)
    return x

goods = []
aPrice = []
bPrice = []
discount = []
produrl = []
prodSize = []

page = 0
while True:
    page = page + 1
    print(page)

    v_url_search = f'{v_url_main}?searchTerm={Search_word}&currentPage={page}&rowsperPage=30&sort=saleCnt&searchType=total#none'
    response = requests.get(v_url_search, headers=HEADER, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    v_lastfound = soup.find("p", attrs={"class": "d-flex justify-content-center text-medium text-bold margin-b-12"})
    if v_lastfound != None :
        break

    prodBox = soup.find('div', attrs={"id":"divList"})
    prodList = prodBox.find_all("div", attrs={"class": "card card-goods"})  # 30
    for product in prodList:
        # product = prodLists[0]

        ProdNames   = product.find("p",      attrs={"class": "card-goods__text"})
        afterPrice  = product.find("strong", attrs={"class": "card-goods__price"})
        beforePrice = product.find("s",      attrs={"class": "card-goods__price"})
        percent     = product.find("strong", attrs={"class": "card-goods__discount"})
        
        v_url_prodDetail = product.find("a", attrs={"class": "card-goods__link"})['href']
        v_url_prodDetail = f'{v_url}{v_url_prodDetail}'

        response = requests.get(v_url_prodDetail, headers=HEADER, verify=False)
        html = response.text
        soup = BeautifulSoup(html, "lxml") 

        sizeBox = soup.find(id="txt_opt_nm") # , elect('')
        sizeBox = sizeBox.find_next_sibling("div")
        sizeList = sizeBox.find_all("li")
        
        availSize = []
        if sizeList != None:
            for eachSize in sizeList:
                # eachSize = sizeList[0]
                if len(eachSize.select('div> img')) == 0:
                    availSize.append(remove_others_to_str(
                        eachSize.find('button').get_text()))
                         

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
#https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=

dresstable = pd.DataFrame({
    'goods':    goods,
    'aprice':  aPrice,
    'bprice':  bPrice,
    'discount': discount
})




