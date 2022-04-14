import requests
from bs4 import BeautifulSoup
import pandas as pd

import fst
fst.LogWd
import sys
import codecs
import pdb
# 1~54
# url = 'https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=%ED%8B%B0%EC%85%94%EC%B8%A0&currentPage=2&rowsperPage=30&sort=saleCnt&statusCd=&lCateId=&cateId=&partner=&color=&size=&season=&minPrice=&maxPrice=&searchType=total#none'
#url = 'https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=%ED%8B%B0%EC%85%94%EC%B8%A0'

# response = requests.get(url, headers=HEADER)
# html = response.text
# soup = BeautifulSoup(html, "lxml") #"html5lib")

# 0th ------
# <div class="card-goods__priceInfo">
# <strong class="card-goods__price">9,900</strong>
# <s class="card-goods__price">12,900</s>
# <strong class="card-goods__discount">23%</strong>
# </div>

# 5th ------
# <div class="card-goods__priceInfo">
# <strong class="card-goods__price">12,900</strong>
# </div>
import urllib3
urllib3.disable_warnings()
# url = 'https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=%ED%8B%B0%EC%85%94%EC%B8%A0&currentPage=2&rowsperPage=30&sort=saleCnt&statusCd=&lCateId=&cateId=&partner=&color=&size=&season=&minPrice=&maxPrice=&searchType=total#none'
URL_main = 'https://www.topten10mall.com/kr/front/search/totalSearch.do'
HEADER = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
#urls = []
# i=1
# for i in range(53):
#     urls.append(f'{URL_main}?searchTerm=티셔츠&currentPage={i}&rowsperPage=30&sort=saleCnt&searchType=total#none')
urls = [
    f'{URL_main}?searchTerm=티셔츠&currentPage={i}&rowsperPage=30&sort=saleCnt&searchType=total#none' for i in range(53)]
#urls = urls[:1]
goods = []
bPrice = []
aPrice = []
discount = []

for url in urls:
    response = requests.get(url, headers=HEADER, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "lxml")  # "html5lib")

    ProdNames = soup.find_all("p", attrs={"class": "card-goods__text"})
    ProdDetails = soup.find_all(
        "div", attrs={"class": "card-goods__priceInfo"})

    for i in range(30):  # i =5
        ProdName = ProdNames[i]
        ProdDetail = ProdDetails[i]
        beforePrice = ProdDetail.select_one("strong.card-goods__price")
        afterPrice = ProdDetail.find("s")
        percent = ProdDetail.select_one("strong.card-goods__discount")

        goods.append(ProdName.get_text() if ProdName != None else 'NoTitle')
        bPrice.append(beforePrice.get_text() if beforePrice != None else 0)
        aPrice.append(afterPrice.get_text() if afterPrice != None else 0)
        discount.append(percent.get_text() if percent != None else 0)


dresstable = pd.DataFrame({
    'goods':    goods,
    'bprice':  bPrice,
    'aprice':  aPrice,
    'discount': discount
})

dresstable.info()

dresstable.dtypes

dresstable.astype({
    'bprice': 'int',
    'aprice': 'int'
})
# dresstable.bprice.str.replace(',', '').astype('int64')
# dresstable['bprice'].apply(lambda x: x.replace(',', ''))
dresstable[['bprice', 'aprice']].apply(lambda x: x.replace(',', ''))
dresstable.iloc[:, [1, 2]].apply(lambda x: x.replace(',', ''))   # X
# dresstable[['bprice', 'aprice']] = dresstable[[
#     'bprice', 'aprice']].apply(lambda x: x.replace(',', ''))


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

dresstable = dresstable.sort_values('discount', ascending=False)



dresstable.to_parquet("myfile.parquet", engine='fastparquet')  # 23
dresstable.to_csv("myfile.csv")  # 92
dresstable.to_csv('mylife2.csv', index=False)                  # 85
dresstable.to_pickle("myfile.pickle")                           # 106

dresstable.to_feather('myfile.ft')                              # 33


store = pd.HDFStore('store.h5')                                 # 96
store['dresstable'] = dresstable  # save it
store['dresstable']  # load it

dresstable[dresstable['bprice'] > 40000].sort_values(
    'discount', ascending=False)

type(dresstable.aprice)


# goods = []
# prices_after  = []
# prices_before = []
# discounts = []

# goods         = soup.find_all("p",      attrs={"class": "card-goods__text"})
# prices_after  = soup.find_all("strong", attrs={"class": "card-goods__price"})
# prices_before = soup.find_all("s",      attrs={"class": "card-goods__price"})
# discounts     = soup.find_all("strong", attrs={"class": "card-goods__discount"})

# dresstable = pd.DataFrame({
#     'goods':         [good.get_text()         for good         in goods][0:29],
#     'prices_after':  [price_after.get_text()  for price_after  in prices_after],
#     'prices_before': [price_before.get_text() for price_before in prices_before],
#     'discounts':     [discount.get_text()     for discount     in discounts]
# })
# print(dresstable.info())


cartoons = soup.find_all("a", attrs={"class": "card-goods__link"})
# cartoons = soup.find_all("p", attrs={"class": "card-goods__text"})
# cartoons = soup.find_all("p", attrs={"class": "strong.card-goods__price"})


for cartoon in cartoons:
    print(cartoon.get_text())
# divList > div:nth-child(1) > div > div > a > p.card-goods__text
# divList > div:nth-child(1) > div > div > a > div
# divList > div:nth-child(1) > div > div > a > div > strong.card-goods__price
# divList > div:nth-child(1) > div > div > a > div > s
# divList > div:nth-child(1) > div > div > a > div > strong.card-goods__discount


sel = []

for i in range(30):
    sel = f"#divList > div:nth-child({i+1}) > div > div > a > p.card-goods__text"


tags = soup.select(sel)
tags


sss = []

ss = cartoons[0].get_text()
sss.extend(ss)

ss = cartoons[1].get_text()
cartoons[2].get_text()


# ui list
news_all = tr_all[1].find_all("li")
for each_tr in news_all:
    text = each_tr.get_text().strip().replace("\n", " ")
    striped_text = re.sub('\s\s+', " ", text)
    print(striped_text)


df = pd.DataFrame([
    ['row1', [ 1, 2, 3, 4, 5]],
    ['row2', [ 6, 7, 8, 9,10]],
    ['row3', [11,12,13,14,15]],
    ['row4', [16,17,18,19,20]]
])

df = pd.DataFrame([
    [ 1,  2,  3,  4,  5],
    [ 6,  7,  8,  9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20]
], index = ['ridx1', 'ridx2', 'ridx3', 'ridx4'],
   columns=['colNm1', 'colNm2', 'colNm3', 'colNm4', 'colNm5'])



df.loc[['ridx1']]         # DataFrame   # df.loc['ridx1']  cf.다른거 Series

df.loc[['ridx1', 'ridx2']   ]
df.loc[['ridx1', 'ridx2'], :]      #same above
df.loc[: , ['colNm1', 'colNm2']]  

df[]

df.loc[0:2]  # same
df.loc[0:2, :]  # same
df.loc[:, 0:2]    # x

df[[0, 1, 2, ]]    # x
df[0:2]
df.iloc[[0, 1]]  # same
df.iloc[0:2]  # same
df.iloc[0:2, :]  # same

df.iloc[:, 0:2]  # all row, slice column
