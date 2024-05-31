from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 웹드라이버 실행
driver = webdriver.Chrome()

driver.get('https://www.adpiamall.com/login')

login_css_selector = "div.login_btn > a"

# 로그인 폼 찾기
username_field = driver.find_element(By.NAME, "mem_id")
password_field = driver.find_element(By.NAME, "mem_pw")

# 로그인 정보 입력
username_field.send_keys('test1')
password_field.send_keys('1111')

element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, login_css_selector)))
element.click()

# 사용자가 프로그램을 종료할 때까지 대기
input("브라우저를 종료하려면 엔터 키를 누르세요...")

# 드라이버 종료
driver.quit()