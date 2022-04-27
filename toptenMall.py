import urllib3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import pdb
import codecs
import sys

Search_word = '반팔티'
v_url = "https://www.topten10mall.com"
v_url_main = f'{v_url}/kr/front/search/totalSearch.do'
urllib3.disable_warnings()
HEADER = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}


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

    v_lastPagefound = soup.find("p", attrs={
                                "class": "d-flex justify-content-center text-medium text-bold margin-b-12"})
    if v_lastPagefound != None:
        break

    prodBox = soup.find('div', attrs={"id": "divList"})
    prodList = prodBox.find_all(
        "div", attrs={"class": "card card-goods"})  # 30
    for product in prodList:
        # product = prodList[0]

        ProdName = product.find("p",      attrs={"class": "card-goods__text"})
        afterPrice = product.find(
            "strong", attrs={"class": "card-goods__price"})
        beforePrice = product.find(
            "s",      attrs={"class": "card-goods__price"})
        percent = product.find(
            "strong", attrs={"class": "card-goods__discount"})

        v_url_prodDetail = product.find(
            "a", attrs={"class": "card-goods__link"})['href']
        v_url_prodDetail = f'{v_url}{v_url_prodDetail}'
        response = requests.get(v_url_prodDetail, headers=HEADER, verify=False)
        html = response.text
        soup = BeautifulSoup(html, "lxml")

        sizeBox = soup.find(id="txt_opt_nm")  # , elect('')
        sizeBox = sizeBox.find_next_sibling("div")
        sizeList = sizeBox.find_all("li")

        availSize = []
        if sizeList != None:
            for eachSize in sizeList:
                # eachSize = sizeList[0]
                if eachSize.find(attrs={'disabled': 'disabled'}) == None:
                    availSize.append(eachSize.find('label').get_text())

        goods.append(ProdName.get_text() if ProdName != None else 'NoTitle')
        aPrice.append(afterPrice.get_text() if afterPrice != None else 0)
        bPrice.append(beforePrice.get_text() if beforePrice != None else 0)
        discount.append(percent.get_text() if percent != None else 0)
        produrl.append(v_url_prodDetail)
        prodSize.append(availSize)

resultTable = pd.DataFrame({
    'goods':    goods,
    'aprice':  aPrice,
    'bprice':  bPrice,
    'discount': discount,
    'url': produrl,
    'availsize': prodSize
})
# dresstable.info()
myTable = resultTable

################################################################################
# Preprocessing
################################################################################
myTable['goods'] = myTable['goods'].apply(lambda x: str(x))
myTable['bprice'] = myTable['bprice'].apply(remove_symbol_to_int)
myTable['aprice'] = myTable['aprice'].apply(remove_symbol_to_int)
myTable['discount'] = myTable['discount'].apply(remove_symbol_to_int)
myTable['url'] = myTable['url']
myTable['availsize'] = myTable['availsize']

# dresstable.to_parquet("myfile.parquet", engine='fastparquet')  # 23
# dresstable.to_csv('mylife2.csv', index=False)                  # 85

df = pd.DataFrame.copy(myTable)
df.info()

################################################################################
# Reshape
# https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html
################################################################################
# explode one list column   cf. melt
# df.explode('availsize')
df = df.explode('availsize')

df.availsize.unique()
# df[df.availsize == '95(XL)']
# df[df.availsize.isin(['80(S)','85(M)','90(L)'])]
# df = df[(df.availsize != '80(S)') & (df.availsize != '85(M)')]
################################################################################
# Filtering
################################################################################

# ----size
#  df[df.availsize.isin(['110', '120', '130', '140', '150', '160'])].values
#  df = df.replace({'availsize': '100'}, {'availsize': '100(XL)'})


df = df[~df.availsize.isnull()]
df = df[~df.availsize.isin(
    ['80', '85', '90', '95', '110', '120', '130', '140', '150', '160'])]


df = df[df.discount != 0]
df = df.loc[-df.goods.str.contains('여성')]
df = df.loc[-df.goods.str.contains('여아')]
df = df.loc[-df.goods.str.contains('남아')]
df = df.loc[-df.goods.str.contains('아동')]
df = df.loc[-df.goods.str.contains('카라')]
df = df[df.aprice>10000]

df.info()
df.shape

df = df.sort_values(['bprice', 'discount'], ascending=False)
df = df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
df.to_csv('./data/sample.txt', index=False, header=None, sep="\t")

import datetime
now = datetime.datetime.now()
current = now.strftime('%m%d_%H%M')
df.to_csv(f'./data/toptenmall_{current}.csv', index=False)
