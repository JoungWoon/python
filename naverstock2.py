import json
import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label

window = Tk()
window.title("Stock Status")
window.geometry("500x500")

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
        stock_info += "(" + str(cnt) + ")" + stock_name + " : " + stock_price + " ( " + stock_icon + stock_up + ")\n"
    window.after(5000, update_stock_info) # 5초마다 업데이트
    label.config(text=stock_info, anchor="w")

label = Label(window, text="Loading...")
label.pack()

window.after(0, update_stock_info) # 5초마다 업데이트
window.mainloop()