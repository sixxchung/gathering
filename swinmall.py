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

while True:
    page = page + 1
    print(page)
    url = f'{URL_main}/search?keyword={Search_word}&page_prd={page}'

    response = requests.get(url, headers=HEADER, verify=False)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    xx = soup.find("div", attrs={"class": "text-center w-100"})
    if xx != None:
        break

    prodList = soup.find("ul", attrs={"id": "prdList"})
    prodLists = prodList.find_all("li")
    # ProdNames = soup.find_all("ul")
    # Prodprod_details = soup.find_all(
    #     "div", attrs={"class": "card-goods__priceInfo"})

    for product in prodLists:
        # product = prodLists[0]

        prodName = product.find("h6",   attrs={"class": "prdli_prdname"})
        afterPrice = product.find(
            "div",  attrs={"class": "d-inline-block font-size-16 font-weight-bold mr-3"})
        beforePrice = product.find(
            "p",    attrs={"class": "color-AAAAAA font-size-14"})
        discountPercent = product.find(
            "span", attrs={"class": "font-weight-bold font-size-16"})

        url_detail = f"https://www.sdmall.com{product.find('a')['href']}"
        # print(url_detail)
        soup_detail = BeautifulSoup(requests.get(
            url_detail, headers=HEADER, verify=False).text, 'lxml')
        prod_detail = soup_detail.find('div', attrs={'id': 'sizeSelectAreaId'})

        if prod_detail != None:
            availSizeList = prod_detail.find_all(
                'div', attrs={'class': 'sizeButtonWrap'})
            availSize = []
            for eachSize in availSizeList:
                # eachSize = availSizeList[0]
                if len(eachSize.select('div> img')) == 0:
                    availSize.append(remove_others_to_str(
                        eachSize.find('button').get_text()))
        else:
            availSize = []

        goods.append(prodName.get_text() if prodName != None else 'NoTitle')
        aPrice.append(afterPrice.get_text() if afterPrice != None else 0)
        bPrice.append(beforePrice.get_text() if beforePrice != None else 0)
        discount.append(discountPercent.get_text()
                        if discountPercent != None else 0)
        produrl.append(url_detail)
        prodSize.append(availSize)

resultTable = pd.DataFrame({
    'goods':    goods,
    'aprice':  aPrice,
    'bprice':  bPrice,
    'discount': discount,
    'url': produrl,
    'availsize': prodSize
})
# myTable.info()

myTable = resultTable
################################################################################
# Preprocessing
################################################################################
myTable['goods'] = myTable['goods'].apply(remove_others_to_str)
myTable['bprice'] = myTable['bprice'].apply(remove_symbol_to_int)
myTable['aprice'] = myTable['aprice'].apply(remove_symbol_to_int)
myTable['discount'] = myTable['discount'].apply(remove_symbol_to_int)
#myTable['url'] = myTable['url']
#myTable['availsize'] = myTable['availsize']

# myTable.info()
myTable.to_parquet("myfile.parquet", engine='fastparquet')  # 23
myTable.to_csv('mylife2.csv', index=False)                  # 85

df = myTable
df.info()







################################################################################
# Filtering
################################################################################
df = df.loc[-df.goods.str.contains('여자')]
# df = df.drop_duplicates(subset=None, keep='first',
#                         inplace=False, ignore_index=False)
# df = df.loc[df.bprice > 40000]
# df = df.loc[df.aprice < 30000]
# df = df.sort_values('discount', ascending=False)

# df.to_csv('df.csv', index=False)

# goodsNm = df.goods[0]
# https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=

################################################################################
# Reshape 
# https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html
################################################################################
# explode one list column   cf. melt
# df.explode('availsize')

dff = df.explode('availsize')

dff.availsize.unique()
# dff[dff.availsize == '95(XL)']
# dff[dff.availsize.isin(['80(S)','85(M)','90(L)'])]
# dff = dff[(dff.availsize != '80(S)') & (dff.availsize != '85(M)')]
dff = dff[~dff.availsize.isin(['80(S)','85(M)','90(L)','95(XL)','여성'])]
dff = dff[~dff.availsize.isnull()]
#dff[dff.availsize == '100'].availsize = '100(XL)'
dff = dff.replace({'availsize': '100'}, {'availsize':'100(XL)'})

# dcast
# pd.crosstab(index=[dff['goods'], dff['aprice'], dff['bprice'],dff['discount'],dff],
#             columns=dff['availsize'])
dfff = pd.crosstab(index=[dff.goods, dff.aprice, dff.bprice, dff.discount, dff.url],
            columns= dff.availsize)
# for col in dfff:
#     print(f'{col} ==>', end='')
#     print(dfff[col].unique())

# dff.pivot_table(index=['goods', 'aprice', 'bprice', 'discount', 'url'],
#             columns=['availsize'], 
#             aggfunc= len).fillna(0)  #values=[dff.availsize])

#dd = (dfff.reset_index)
################################################################################
# Filtering
################################################################################
dd = dfff[(dfff['95(L)']==1) | (dfff['100(XL)']==1)]
dd01 = dd.reset_index()
dd02 = dd01.iloc[:,0:5]

dd02.to_csv('./data/swimmall.csv', index=False) 

# ------------------------------------------------------------------------------
import matplotlib.pyplot as plt
fig = plt.Figure()
from plotnine import *  # ggplot
(
    ggplot(aes(x='bprice'), data=dd01) + geom_bar(stat="count")
)
(
    ggplot(aes(x='bprice',y='aprice'), data=dd01)
    + geom_point()
)

# ------------------------------------------------------------------------------
import plotly.graph_objs as go
import plotly.express as px

gdf = dd02.groupby('discount').count().reset_index()
dd02.aprice.unique()
gdf = dd02.groupby('aprice').count().reset_index()

fig = px.bar(gdf, x='aprice', y='goods')
fig.show()

fig = px.scatter(dd02, x='bprice', y='aprice')

dd02[dd02.bprice>80000]

# df = df.drop_duplicates(subset=None, keep='first',
#                         inplace=False, ignore_index=False)
# df = df.loc[df.bprice > 40000]
# df = df.loc[df.aprice < 30000]
# df = df.sort_values('discount', ascending=False)

# df.to_csv('df.csv', index=False)
data_canada = px.data.gapminder().query("country == 'Canada'")
