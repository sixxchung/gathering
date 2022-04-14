# https://bill1224.tistory.com/251?category=785358

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



