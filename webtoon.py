import requests
from bs4 import BeautifulSoup
import lxml

url = "https://comic.naver.com/webtoon/weekday.nhn"
res = requests.get(url)
res.raise_for_status()  # 문제있을 경우 프로그램 종료

soup = BeautifulSoup(res.text, "lxml")
#soup = BeautifulSoup(res.text, "html5lib")
# 네이버 웹툰 목록 전체 가져오기
cartoons = soup.find_all("a", attrs={"class": "title"})
# find_all : class가 title인  모든 "a" element를 반환
for cartoon in cartoons:
    print(cartoon.get_text())