import requests
from bs4 import BeautifulSoup

# 1~54
url = 'https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=%ED%8B%B0%EC%85%94%EC%B8%A0&currentPage=1&rowsperPage=30&sort=saleCnt&statusCd=&lCateId=&cateId=&partner=&color=&size=&season=&minPrice=&maxPrice=&searchType=total#none'
url = 'https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=%ED%8B%B0%EC%85%94%EC%B8%A0&currentPage=2&rowsperPage=30&sort=saleCnt&statusCd=&lCateId=&cateId=&partner=&color=&size=&season=&minPrice=&maxPrice=&searchType=total#none'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "lxml") #"html5lib")

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

dress_prices = []
dress_names = []
dress_links = []


soup = BeautifulSoup(url.text, 'html.parser')
prices = soup.select(".price .num")
dress_price = [price.text for price in prices]
dress_prices.extend(dress_price)

dresstable = pd.DataFrame({'names': dress_names,
'prices': dress_prices,
'link': dress_links
})
print(dresstable.info())


import re
m = re.search('(?<=abc)ef', 'al;kdjf;laekrjncvj;lkadfj;abcdef')
m.group(0)



m = re.search(r'(?<=-)\w+', 'spam-egg')


import re
text = "에러 1122 : 레퍼런스 오류\n 에러 1033: 아규먼트 오류"
regex = re.compile("에러 1033")
mo = regex.search(text)
if mo != None:
    print(mo.group()) 

import re
regex = re.compile('[a-z]+')

import re
regex = re.compile('[a-z]+')   # 패턴객체 regex만들기
matchObj = regex.match('python a ajkb pattern')
if matchObj != None:
    result = matchObj.group()          # 검사할문장에서 패턴매치된 문자열 리턴
else:
    result = "Not Found!!"
print(result)