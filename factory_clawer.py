import os
import time
from selenium import webdriver
from selenium.common import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

download_path = r'D:\Users\user\Downloads'

state= False
# 设置Firefox的下载偏好
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)  # 0代表下载到桌面；1代表下载到默认目录；2代表下载到指定目录。
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", download_path)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # MIME类型改为您期望自动下载文件的类型。

# 初始化Firefox WebDriver
options = Options()
driver = webdriver.Firefox(options=options)
driver.get("https://dmz26.moea.gov.tw/GMWeb/investigate/InvestigateFactory.aspx") # 更改網址以前往不同網頁
time.sleep(1)
type_selector = {}
area = {}

def clawer_type_selector(driver):
    num = 2
    while True:
        try:
            element_id = f'ContentPlaceHolder1_tvFactoryKindn{num}CheckBox'
            a = driver.find_element(By.XPATH, f"//*[@id='{element_id}']//following-sibling::*")
            type_selector[a.text] = element_id
            num += 1
        except Exception as e:
            print(f"抓取產業元素完畢: {e}")
            break
def clawer_area(driver):
    num = 1
    while True:
        try:
            element_id = f'ContentPlaceHolder1_tvFactoryCityn{num}CheckBox'
            a = driver.find_element(By.XPATH, f"//*[@id='{element_id}']//following-sibling::*")
            area[a.text] = element_id
            num += 1
        except Exception as e:
            print(f"抓取地區元素完畢: {e}")
            break


# clawer_type_selector(driver)
# clawer_area(driver)
# print(area)
# print(type_selector)
# df1 = pd.DataFrame(list(area.items()), columns=['area', 'area_Value'])
#
# df2 = pd.DataFrame(list(type_selector.items()), columns=['type', 'type_Value'])
#
# # result = pd.concat([df1, df2], axis=1)
# df1.to_excel('area.xlsx', index=False, engine='openpyxl')
# df2.to_excel('type.xlsx', index=False, engine='openpyxl')
data = pd.read_excel('area.xlsx')
data1 = pd.read_excel('type.xlsx')
df1 = pd.DataFrame(data=data)
df2 = pd.DataFrame(data=data1)

for index2, row2 in df2.iterrows():
    # 遍历df1中的每一行
    for index1, row1 in df1.iterrows():
        # 根据column1的字符进行匹配以及column2的值进行乘法运算
        area_id = row1['area_Value']
        try:
            time.sleep(2)
            button = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_btnReset"]')
            button.click()
            checkbox = driver.find_element(By.ID, area_id)
            if not checkbox.is_selected():
                checkbox.click()
            type_selector_id = row2['type_Value']
            checkbox = driver.find_element(By.ID, type_selector_id)
            if not checkbox.is_selected():
                checkbox.click()
            submit=driver.find_element(By.XPATH,"//*[@id='ContentPlaceHolder1_btnFactoryQuery']")
            submit.click()
            time.sleep(5)
            state = True
        except Exception as e:
            print(e)
            try:
                WebDriverWait(driver, 60).until(EC.alert_is_present())
                # 切换到alert
                alert = driver.switch_to.alert
                # 打印弹窗文本
                print("Alert present: " + alert.text)
                # 点击"确定"按钮来关闭alert弹窗
                alert.accept()
                print("Alert has been accepted.")
            except NoAlertPresentException:
                print("No alert present.")


        try:
            while state:
                submit = driver.find_element(By.XPATH, "//*[@id='ContentPlaceHolder1_btnDownloadListReport']")
                submit.click()
                new_filename = f'{row1['area']}_{row2['type']}.xls'
                original_filename = 'Factory_list.xls'  # 假定下载的文件名
                original_file_path = os.path.join(download_path, original_filename)
                new_file_path = os.path.join(download_path, new_filename)
                timeout = 60  # 超时时间，单位秒
                end_time = time.time() + timeout



                # 列出下载目录中的所有文件
                files = os.listdir(download_path)

                # 检查是否有文件名以预期的前缀开始
                file_found = any(file.startswith(original_filename) for file in files)
                if file_found:
                    print("File has been downloaded.")
                    os.rename(original_file_path, new_file_path)
                    print(f"File renamed to {new_filename}")
                    button = driver.find_element(By.XPATH, "//*[@id='btnBackQuery']")
                    button.click()
                    time.sleep(2)
                    state = False
                    break
                elif time.time() > end_time:
                    print("Timed out waiting for the file to download.")
                    break
        except Exception as e:
            print(e)
driver.close() # 關閉瀏覽器視窗
