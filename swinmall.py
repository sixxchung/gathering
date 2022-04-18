import urllib3
import requests
from bs4 import BeautifulSoup
import pandas as pd

import pdb
import codecs
import sys

# 1~54
Search_word = '제이커스'
URL_main = 'https://www.sdmall.com/'
page = 0

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
# url = urls[6]
#for url in urls:
prodSize=[]
while True:
    page = page + 1
    print(page)
    url = f'{URL_main}/search?keyword={Search_word}&page_prd={page}'
    
    response = requests.get(url, headers=HEADER, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    xx = soup.find("div", attrs={"class": "text-center w-100"})
    if xx != None :
        break
    ProdList = soup.find("ul", attrs={"id":"prdList"})
    ProdLists = ProdList.find_all("li")
    # ProdNames = soup.find_all("ul")
    # ProdDetails = soup.find_all(
    #     "div", attrs={"class": "card-goods__priceInfo"})

    for product in ProdLists:
        # product = ProdLists[0]

        prodName        = product.find("h6",   attrs={"class":"prdli_prdname"})
        afterPrice      = product.find("div",  attrs={"class":"d-inline-block font-size-16 font-weight-bold mr-3"}) 
        beforePrice     = product.find("p",    attrs={"class":"color-AAAAAA font-size-14"})
        discountPercent = product.find("span", attrs={"class":"font-weight-bold font-size-16"})
        
        urlDetail = f"https://www.sdmall.com{product.find('a')['href']}"
        print(urlDetail)
        soupDetail = BeautifulSoup(requests.get(urlDetail, headers=HEADER, verify=False).text, 'lxml')
        Detail = soupDetail.find('div', attrs={'id':'sizeSelectAreaId'})
        if Detail != None:
            sizelist = Detail.find_all('div', attrs={'class':'sizeButtonWrap'})
            availableSize = []
            for eachSize in sizelist:
                # eachSize = sizelist[0]
                if len(eachSize.select('div> img'))>0 :
                    availableSize.append( remove_others_to_str(eachSize.find('button').get_text()))
                else:
                    availableSize = []
        else:
            availbleSize = []

        goods.append(prodName.get_text() if prodName != None else 'NoTitle')
        aPrice.append(afterPrice.get_text() if afterPrice != None else 0)
        bPrice.append(beforePrice.get_text() if beforePrice != None else 0)
        discount.append(discountPercent.get_text() if discountPercent != None else 0)
        prodSize.append(availableSize)

resultTable = pd.DataFrame({
    'goods':    goods,
    'aprice':  aPrice,
    'bprice':  bPrice,
    'discount': discount,
    'size': prodSize 
})
# myTable.info()

myTable = resultTable


myTable['goods']    = myTable['goods'].apply(remove_others_to_str)
myTable['bprice']   = myTable['bprice'].apply(remove_symbol_to_int)
myTable['aprice']   = myTable['aprice'].apply(remove_symbol_to_int)
myTable['discount'] = myTable['discount'].apply(remove_symbol_to_int)
myTable['size']     = myTable['size']
#dresstable.info()

# dresstable.to_parquet("myfile.parquet", engine='fastparquet')  # 23
# dresstable.to_csv('mylife2.csv', index=False)                  # 85

df = myTable
df.info()

# ----------------------------------------------------------

df = df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
df = df.loc[df.bprice > 40000]
df = df.loc[df.aprice < 30000]
df = df.loc[-df.goods.str.contains('여자수영복')]
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




