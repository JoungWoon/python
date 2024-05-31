import json
import requests
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from datetime import datetime

# 메인 윈도우 생성
root = tk.Tk()
root.title("주요 주식 종목 현황")
root.geometry("800x500")

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

# Frame을 사용하여 Treeview 및 사용자 정의 헤더를 포함할 컨테이너 생성
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# Canvas를 사용하여 사용자 정의 헤더를 추가
canvas = tk.Canvas(frame, height=30, bg="lightblue")
canvas.pack(side="top", fill="x")

# Treeview 위젯 생성
tree = ttk.Treeview(frame)

# Treeview의 기본 헤더 숨기기
style = ttk.Style()
style.configure("Custom.Treeview.Heading", font=("Arial", 12), padding=10)
style.layout("Custom.Treeview", [("Custom.Treeview.treearea", {"sticky": "nswe"})])

# 컬럼 정의
tree["columns"] = ("price", "icon", "up", "date")

# 사용자 정의 헤더 추가
canvas.create_text(105, 15, text="종목명", font=("Arial", 12, "bold"), anchor="w")
canvas.create_text(250, 15, text="현재가", font=("Arial", 12, "bold"), anchor="w")
canvas.create_text(475, 15, text="증감액", font=("Arial", 12, "bold"), anchor="w")
canvas.create_text(675, 15, text="업데이트시간", font=("Arial", 12, "bold"), anchor="w")

# Treeview 배치
tree.pack(side="top", fill="both", expand=True)

# 샘플 데이터 추가

# 데이터 삽입
def update_stock_info():
    global cnt
    stock_info = ""
    cnt += 1
    for code in codes:
        bs_obj = get_bs_obj(code)
        stock_name = get_stock_name(bs_obj)
        stock_price = get_current_price(bs_obj)
        stock_icon = get_price_change_icon(bs_obj)
        stock_up = get_stock_up(bs_obj)
        stock_ad = stock_icon + stock_up
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

         # 현재 트리뷰 아이템을 저장하는 딕셔너리
        existing_items = {tree.item(item)["text"]: item for item in tree.get_children()}


         # 주식 이름이 기존 항목에 있는지 확인
        if stock_name in existing_items:
            # 기존 항목 업데이트
            tree.item(existing_items[stock_name], values=(stock_price, stock_ad, current_time))
        else:
            # 새로운 항목 추가
            tree.insert("", "end", text=stock_name, values=(stock_price, stock_ad, current_time))
    root.after(5000, update_stock_info) # 5초마다 업데이트


root.after(0, update_stock_info) # 5초마다 업데이트

# 메인 루프 시작
root.mainloop()
