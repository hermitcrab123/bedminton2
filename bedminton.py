from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

target_time = datetime(2024, 10, 24, 23, 49, 50)

options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 等待直到目标时间
while True:
    current_time = datetime.now()
    if current_time >= target_time:
        break
    time.sleep(0.1)  # 每0.1秒检查一次

driver = webdriver.Chrome(options=options)
driver.get("https://scr.cyc.org.tw/tp10.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D=2024/11/09&D2=1")

# 定义点击和按下 Enter 键的操作
def click_and_enter():
    element = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_Step2_data"]/table/tbody/tr[17]/td[3]/img')
    element.click()  # 点击元素
    
    

# 处理弹出框的函数
def handle_alert():
    try:
        # 等待警告框出現
        alert = driver.switch_to.alert
        alert.accept()  # 接受警告（点击确认）
        ActionChains(driver).send_keys('\n').perform()  # 按下 Enter 键
        print("警告已处理")
    except NoAlertPresentException:
        print("没有弹出警告")
    except UnexpectedAlertPresentException:
        print("意外的警告出现")
        ActionChains(driver).send_keys('\n').perform()
    except TimeoutException:
        print("等待警告框超时")

# 重试逻辑
while True:
    try:
        click_and_enter()  # 尝试点击并按下 Enter
        handle_alert()     # 处理弹出警告
        print("成功点击并按下 Enter 键！")
        break  # 如果成功，退出循环
    except Exception as e:
        print(f"发生错误：{e}，正在重试...")
        time.sleep(10)  # 等待一秒后重试
