import sys
import requests
from bs4 import BeautifulSoup

# 웹 페이지 요청
url = 'https://news.naver.com/section/105'
response = requests.get(url)

# BeautifulSoup으로 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 제외할 구문 리스트 설정
exclude_phrases = ["기사", "모음"]

# 제목과 링크 저장을 위한 리스트
titles_and_links = []

# 기사 제목 추출
for title in soup.find_all('p', class_='rl_txt'):
    parent_div  = title.find_parent('div', class_='rl_link_end')
    if not any(phrase in title.text for phrase in exclude_phrases):
        sibling_a_tags  =  parent_div.find_all('a', recursive=False)
        for a_tag in sibling_a_tags:
            href = a_tag['href']
            titles_and_links.append((title.text, href))

# 제목 출력 및 사용자가 선택
for idx, (title, link) in enumerate(titles_and_links):
    print(f"{idx + 1}: {title}")

selected_idx = int(input("기사를 선택하세요 (번호 입력): ")) - 1
selected_title, selected_link = titles_and_links[selected_idx]

print(f"선택한 기사: {selected_title}")
print(f"링크: {selected_link}")

# 기사 내용 가져오기
article_url = selected_link
article_response = requests.get(article_url)
article_soup = BeautifulSoup(article_response.text, 'html.parser')

# 기사 내용을 담고 있는 태그 찾기 (예: div, class='article_body')
article_body = article_soup.find('article', class_='go_trans _article_content')
if article_body:
    content = article_body.get_text(strip=True)
    print(f"내용: {content}")
else:
    print("기사 내용을 찾을 수 없습니다.")