import json
import requests
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from datetime import datetime

# 메인 윈도우 생성
root = tk.Tk()
root.title("주요 주식 종목 현황")

codes = ['005930', '010130','371460','381180'] # 종목코드 리스트
prices = [] # 가격정보가 담길 리스트
cnt = 0

def get_bs_obj(item_code):
    url = "https://finance.naver.com/item/main.nhn?code="+item_code
    raw_data = requests.get(url)
    bs_obj = BeautifulSoup(raw_data.content, "html.parser", from_encoding='euc-kr')
    return bs_obj

def get_current_price(obj):
    no_today = obj.find("p", {"class":"no_today"})
    blind_now = no_today.find("span", {"class":"blind"})
    return blind_now.text


def get_first_price(obj):
    no_down = obj.find("td", {"class":"first"})
    blind_now = no_down.find("span", {"class":"blind"})
    return blind_now.text


def get_stock_name(obj):
    company = obj.find("a", onclick="clickcr(this, 'sop.title', '', '', event);window.location.reload();")
    return company.text

def get_stock_up(obj):
    no_up = obj.find("p", {"class":"no_exday"})
    blind_now = no_up.find("span", {"class":"blind"})
    return blind_now.text


def get_price_change_icon(obj):
    icon_minus = obj.find("span", {"class":"minus"})
    icon_plus = obj.find("span", {"class":"plus"})

    if icon_minus:
        return "-"
    elif icon_plus:
        return "+"
    else:
        return ""


# Treeview 위젯 생성
tree = ttk.Treeview(root)

# 컬럼 정의
tree["columns"] = ("one", "onetwo", "two","three")

# 컬럼 설정
tree.column("#0", width=250, minwidth=200)
tree.column("one", width=150, minwidth=100)
tree.column("onetwo", width=150, minwidth=100)
tree.column("two", width=150, minwidth=100)
tree.column("three", width=150, minwidth=100)

# 컬럼 헤더 설정
tree.heading("#0", text="종목명", anchor=tk.W)
tree.heading("one", text="현재가", anchor=tk.W)
tree.heading("onetwo", text="전일가", anchor=tk.W)
tree.heading("two", text="증감액", anchor=tk.W)
tree.heading("three", text="업데이트시간", anchor=tk.W)

# 데이터 삽입
def update_stock_info():
    global cnt
    stock_info = ""
    cnt += 1
    for code in codes:
        bs_obj = get_bs_obj(code)
        stock_name = get_stock_name(bs_obj)
        stock_price = get_current_price(bs_obj)
        stock_first_price = get_first_price(bs_obj)
        stock_icon = get_price_change_icon(bs_obj)
        stock_up = get_stock_up(bs_obj)
        stock_ad = stock_icon + stock_up
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

         # 현재 트리뷰 아이템을 저장하는 딕셔너리
        existing_items = {tree.item(item)["text"]: item for item in tree.get_children()}


         # 주식 이름이 기존 항목에 있는지 확인
        if stock_name in existing_items:
            # 기존 항목 업데이트
            tree.item(existing_items[stock_name], values=(stock_price, stock_first_price, stock_ad, current_time))
        else:
            # 새로운 항목 추가
            tree.insert("", "end", text=stock_name, values=(stock_price, stock_first_price, stock_ad, current_time))
    root.after(5000, update_stock_info) # 5초마다 업데이트


# Treeview 배치
tree.pack(side="top", fill="both", expand=True)


root.after(0, update_stock_info) # 5초마다 업데이트

# 메인 루프 시작
root.mainloop()
