# https://bill1224.tistory.com/251?category=785358
URL_main= "aa"
i =1
f'{URL_main}?searchTerm=%ED%8B%B0%EC%85%94%EC%B8%A0&currentPage={i}&
rowsperPage=30&
sort=saleCnt&statusCd=&
lCateId=&
cateId=&
partner=&
color=&
size=&
season=&
minPrice=&
maxPrice=&
searchType=total#none'

import requests
from bs4 import BeautifulSoup
headers = {"user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
url = 'https://www.topten10mall.com/kr/front/search/totalSearch.do?searchTerm=%ED%8B%B0%EC%85%94%EC%B8%A0'
res = requests.get(url, headers=headers)
#res = requests.get(url)
if res.status_code !=200 : # requests.codes.ok
    print(f"error occur [error code {res.status_code}]")
print(res.raise_for_status())

html = res.text
soup = BeautifulSoup(html, "html5lib")


# pandas와 numpy의 import
import pandas as pd
import numpy as np

# 예제용 배열 선언
ex_df = pd.DataFrame([[0, 1, 3], [0, 2, 4], [0, 3, 3], [
                            1, 2, 3]], columns=['c0', 'c1', 'c2'])

ex_df

ex_df.duplicated(subset=['c0'])

ex_df.drop_duplicates(subset=)

Index(['c0'])

   c0  c1  c2

0   0   1   3

3   1   2   3
