from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup

app = FastAPI()
templates = Jinja2Templates(directory="template")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # 뉴스 섹션 URL
    url = 'https://news.naver.com/section/105'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 제외할 구문 리스트 설정
    exclude_phrases = ["기사", "모음"]

    # 제목과 링크 저장을 위한 리스트
    titles_and_links = []

    # 특정 <p> 태그 이후 오는 <a> 태그의 href 추출
    for title in soup.find_all('p', class_='rl_txt'):
        parent_div  = title.find_parent('div', class_='rl_link_end')
        if not any(phrase in title.text for phrase in exclude_phrases):
            sibling_a_tags  =  parent_div.find_all('a', recursive=False)
            for a_tag in sibling_a_tags:
                href = a_tag['href']
                titles_and_links.append((title.text, href))

    return templates.TemplateResponse("index.html", {"request": request, "titles_and_links": titles_and_links})

@app.get("/article", response_class=HTMLResponse)
async def article(request: Request, url: str):
    article_response = requests.get(url)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

    # 기사 내용을 담고 있는 태그 찾기 (예: div, class='article_body')
    article_body = article_soup.find('article', class_='go_trans _article_content')
    if article_body:
        #content = article_body.get_text(strip=True)
        content = article_body
    else:
        content = "기사 내용을 찾을 수 없습니다."

    return templates.TemplateResponse("article.html", {"request": request, "content": content})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
