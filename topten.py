import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1~54
url = 'https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=%ED%8B%B0%EC%85%94%EC%B8%A0&currentPage=1&rowsperPage=30&sort=saleCnt&statusCd=&lCateId=&cateId=&partner=&color=&size=&season=&minPrice=&maxPrice=&searchType=total#none'
#url = 'https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=%ED%8B%B0%EC%85%94%EC%B8%A0&currentPage=2&rowsperPage=30&sort=saleCnt&statusCd=&lCateId=&cateId=&partner=&color=&size=&season=&minPrice=&maxPrice=&searchType=total#none'

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "lxml") #"html5lib")



#0th ------
# <div class="card-goods__priceInfo">
# <strong class="card-goods__price">9,900</strong>
# <s class="card-goods__price">12,900</s>
# <strong class="card-goods__discount">23%</strong>
# </div>

#5th ------
# <div class="card-goods__priceInfo">
# <strong class="card-goods__price">12,900</strong>
# </div>

urls = []
for i in range(53):
    urls.append(f'https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=%ED%8B%B0%EC%85%94%EC%B8%A0&currentPage={i}&rowsperPage=30&sort=saleCnt&statusCd=&lCateId=&cateId=&partner=&color=&size=&season=&minPrice=&maxPrice=&searchType=total#none')


goods = []
bPrice  = []
aPrice = []
discount = []
for url in urls:
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "lxml") #"html5lib")

    ProdNames = soup.find_all("p", attrs={"class":"card-goods__text"})
    ProdDetails= soup.find_all("div", attrs={"class":"card-goods__priceInfo"})

    for i in range(30):  # i =5
        ProdName = ProdNames[i]
        ProdDetail = ProdDetails[i]
        beforePrice = ProdDetail.select_one("strong.card-goods__price")
        afterPrice  = ProdDetail.find("s") 
        percent    = ProdDetail.select_one("strong.card-goods__discount") 
        
        goods.append( ProdName.get_text() if ProdName!=None else 'NoTitle' )
        bPrice.append( beforePrice.get_text() if beforePrice!=None else 0)
        aPrice.append( afterPrice.get_text()  if afterPrice!=None else 0)
        discount.append( percent.get_text() if percent!=None    else 0)


dresstable = pd.DataFrame({
    'goods':    goods,
    'bPrice':  bPrice,
    'aPrice':  aPrice,
    'discount': discount
})
print(dresstable.info())






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
#divList > div:nth-child(1) > div > div > a > p.card-goods__text
#divList > div:nth-child(1) > div > div > a > div
#divList > div:nth-child(1) > div > div > a > div > strong.card-goods__price
#divList > div:nth-child(1) > div > div > a > div > s
#divList > div:nth-child(1) > div > div > a > div > strong.card-goods__discount







sel =[]

for i in range(30):
    sel = f"#divList > div:nth-child({i+1}) > div > div > a > p.card-goods__text"
    

tags = soup.select(sel)
tags


sss =[]

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

