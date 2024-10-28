from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, TimeoutException
import time
from datetime import datetime

# 設定目標時間
target_time = datetime(2024, 10, 28, 23, 59, 59)

# 設定 Chrome 瀏覽器選項
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# 等待直到目標時間
while True:
    current_time = datetime.now()
    if current_time >= target_time:
        break
    time.sleep(0.1)  # 每0.1秒檢查一次

# 初始化 Chrome 瀏覽器
driver = webdriver.Chrome(options=options)

# 定義導航到目標網頁的函數
def navigate_to_page():
    driver.get("https://scr.cyc.org.tw/tp10.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D=2024/11/11&D2=3")

# 定義查找可點擊元素的操作
def find_and_click_available_element(tr_range):
    elements = []  # 初始化元素列表
    # 獲取指定範圍內的所有符合條件的元素
    for position in range(tr_range[0], tr_range[1] + 1):
        elements += driver.find_elements(By.XPATH, f'//*[@id="ContentPlaceHolder1_Step2_data"]/table/tbody/tr[{position}]/td[3]/img')

    # 遍歷找到的元素
    for element in elements:
        text = element.get_attribute("title")  # 獲取該元素的標題文本
        
        # 判斷元素是否已被預約
        if "已被預約" in text:
            print(f"找到已被預約的元素: {text}")
            continue  # 若已被預約，則跳過此元素
        else:
            print(f"找到可預約的元素: {text}")
            element.click()  # 點擊可預約的元素
            return True  # 成功點擊，返回 True

    return False  # 如果沒有可預約的元素，返回 False

# 處理彈出框的函數
def handle_alert():
    try:
        alert = driver.switch_to.alert  # 切換到彈出警告框
        alert.accept()  # 接受警告（點擊確認）
        print("警告已處理")
    except NoAlertPresentException:
        print("沒有彈出警告")
    except UnexpectedAlertPresentException:
        print("意外的警告出現")
        alert = driver.switch_to.alert
        alert.accept()
    except TimeoutException:
        print("等待警告框超時")

# 定義 tr 組的範圍
tr_groups = [(10, 13), (16, 19), (22, 25)]
last_group_index = -1  # 初始化上次成功的組索引

# 成功計數器
success_count = 0

# 重試邏輯
while True:
    navigate_to_page()  # 每次運行前導航到網頁

    for i in range(last_group_index + 1, len(tr_groups)):
        try:
            # 嘗試查找並點擊可用元素
            if find_and_click_available_element(tr_groups[i]):
                handle_alert()  # 處理彈出警告
                print("成功點擊並處理警告！")
                last_group_index = i  # 更新上次成功的組索引
                success_count += 1  # 增加成功計數
                if success_count == 2:  # 如果成功次數達到2，終止程序
                    print("已成功執行兩次，程序即將終止。")
                    exit()  # 终止程序
                break  # 退出內層循環
            else:
                print(f"在組 {tr_groups[i]} 的所有元素已被預定，嘗試下一個組...")
                continue
        except Exception as e:
            print(f"發生錯誤：{e}，正在重試...")
            time.sleep(10)

    else:
        print("所有組的元素均已被預定，稍後重試...")
        time.sleep(10)  # 等待一段時間後重試
        continue
