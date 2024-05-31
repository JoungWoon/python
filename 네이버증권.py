import json
import requests
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from bs4 import BeautifulSoup
from datetime import datetime

# 종목코드 파일명
CODES_FILE = "stock_codes.txt"

def save_codes(filename, codes):
    with open(filename, 'w') as f:
        for code in codes:
            f.write(code + '\n')

def load_codes(filename):
    codes = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                codes.append(line.strip())
    except FileNotFoundError:
        pass
    return codes

# 새로운 종목코드를 입력받아 리스트에 추가하고 Treeview를 업데이트하는 함수
def add_code():
    new_code = simpledialog.askstring("Input", "Enter a new stock code:")
    if new_code:
        if new_code in codes:
            messagebox.showwarning("Warning", "This stock code already exists.")
        else:
            codes.append(new_code)
            save_codes(CODES_FILE, codes)
            bs_obj = get_bs_obj(new_code)
            stock_name = get_stock_name(bs_obj)
            messagebox.showinfo("Info", f"{stock_name} 추가")
            root.after(0, update_stock_info)

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

def get_trading_count(obj):
    return (obj.find("span", string='거래량')
                .find_next_sibling('em')
                .find("span", class_="blind")
                .get_text()
            if obj.find("span", string='거래량')
            else '')

def get_asking_sell_count(obj):
    return (obj.find("tr", class_='total')
                .find("td", class_="f_down")
                .get_text(strip=True))

def get_asking_buy_count(obj):
    return (obj.find("tr", class_='total')
                .find("td", class_="f_up")
                .get_text(strip=True))

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

# 초기 종목코드 리스트를 파일에서 읽어옴
codes = load_codes(CODES_FILE)
prices = [] # 가격정보가 담길 리스트
cnt = 0


# 메인 윈도우 생성
root = tk.Tk()
root.title("Stock Code Manager")
#root.geometry("1024x600")
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Treeview 생성
# Treeview 위젯 생성
# Treeview 위젯 생성
tree = ttk.Treeview(frame)
# 새로운 종목코드를 추가하는 버튼
add_button = tk.Button(root, text="Add Stock Code", command=add_code)
add_button.pack(pady=10)

# 프로그램 종료 버튼
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=10)

# 컬럼 정의
tree["columns"] = ("one", "onetwo", "two","two1", "two2","two3","two4","three")

# 컬럼 설정
tree.column("#0", width=250, minwidth=200)
tree.column("one", width=150, minwidth=100)
tree.column("onetwo", width=150, minwidth=100)
tree.column("two", width=150, minwidth=100)
tree.column("two1", width=150, minwidth=100)
tree.column("two2", width=150, minwidth=100)
tree.column("two3", width=150, minwidth=100)
tree.column("two4", width=150, minwidth=100)
tree.column("three", width=150, minwidth=100)

# 컬럼 헤더 설정
tree.heading("#0", text="종목명", anchor=tk.W)
tree.heading("one", text="현재가", anchor=tk.W)
tree.heading("onetwo", text="전일가", anchor=tk.W)
tree.heading("two", text="전일대비", anchor=tk.W)
tree.heading("two1", text="등락율", anchor=tk.W)
tree.heading("two2", text="거래량", anchor=tk.W)
tree.heading("two3", text="호가매도잔량", anchor=tk.W)
tree.heading("two4", text="호가매수잔량", anchor=tk.W)
tree.heading("three", text="업데이트시간", anchor=tk.W)



# 데이터 삽입
def update_stock_info():
    global cnt
    cnt += 1
    for code in codes:
        bs_obj = get_bs_obj(code)
        stock_name = get_stock_name(bs_obj)
        stock_price = get_current_price(bs_obj)
        stock_trade = get_trading_count(bs_obj)
        stock_asking_sell_count = get_asking_sell_count(bs_obj)
        stock_asking_buy_count = get_asking_buy_count(bs_obj)
        stock_first_price = get_first_price(bs_obj)
        stock_icon = get_price_change_icon(bs_obj)
        stock_up = get_stock_up(bs_obj)
        stock_percent = int(stock_up.replace(",", "")) / int(stock_first_price.replace(",", ""))
        stock_percent = round(stock_percent, 4) * 100
        stock_percent = str(round(stock_percent, 2)) + '%'
        stock_percent = stock_icon + stock_percent

        stock_ad = stock_icon + stock_up
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

         # 현재 트리뷰 아이템을 저장하는 딕셔너리
        existing_items = {tree.item(item)["text"]: item for item in tree.get_children()}

         # 주식 이름이 기존 항목에 있는지 확인
        if stock_name in existing_items:
            # 기존 항목 업데이트
            tree.item(existing_items[stock_name], values=(stock_price, stock_first_price, stock_ad, stock_percent, stock_trade, stock_asking_sell_count, stock_asking_buy_count, current_time))
        else:
            # 새로운 항목 추가
            tree.insert("", "end", text=stock_name, values=(stock_price, stock_first_price, stock_ad, stock_percent, stock_trade, stock_asking_sell_count, stock_asking_buy_count, current_time))
    root.after(60000, update_stock_info) # 60초마다 업데이트

# Scrollbar 생성
scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")

# Treeview와 Scrollbar 연결
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)

root.after(0, update_stock_info) # 5초마다 업데이트

# 메인 루프 실행
root.mainloop()
