import requests
from bs4 import BeautifulSoup

# 웹 페이지 요청
url = 'https://news.naver.com/section/105'
response = requests.get(url)

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 제외할 구문 리스트 설정
exclude_phrases = ["기사", "모음"]

# 기사 제목 추출
for title in soup.find_all('p', class_='rl_txt'):
    if not any(phrase in title.text for phrase in exclude_phrases):
        print(title.text)
