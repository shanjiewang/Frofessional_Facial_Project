# 操作 browser 的 API
from selenium import webdriver

# 處理逾時例外的工具
from selenium.common.exceptions import TimeoutException

# 面對動態網頁，等待某個元素出現的工具，通常與 exptected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait

# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC

# 期待元素出現要透過什麼方式指定，通常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# 強制等待 (執行期間休息一下)
from time import sleep

# 執行 command 的時候用
# 處理下拉式選單的工具
from selenium.webdriver.support.ui import Select
import requests
import json
import os
import csv
import re
import urllib
import pandas as pd
import numpy as np

# 處理下拉式選單的工具
from selenium.webdriver.support.ui import Select

# 啟動瀏覽器工具的選項
options = webdriver.ChromeOptions()
# options.add_argument("--headless")                #不開啟實體瀏覽器背景執行
options.add_argument("--start-maximized")  # 最大化視窗
options.add_argument("--incognito")  # 開啟無痕模式
options.add_argument("--disable-popup-blocking ")  # 禁用彈出攔截

driver_path = Service('D:chromedriver.exe')

# 啟動driver
driver = webdriver.Chrome(
    options=options,
    service=driver_path
)

photolimit = 3  # 要存幾張照片
listLink = []

# 百度下載圖片(台灣上市上櫃公司)


def visit():
    global i
    # 前往指定連結 如果只用百度網址會出現  Message: element not interactable 參考 https://blog.csdn.net/gufenchen/article/details/90274169
    driver.get('https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1643049528175_R&pv=&ic=0&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=&ie=utf-8&sid=&word=222')
# csv如果要直接修改內文要用txt開啟 再選擇'具有BOM的utf-8'存成csv檔
    df = pd.read_csv(r'Csvs/china500nameList_f.csv')
    print(len(df))

    # 篩選含空值的行
    df[df.isnull().values == True].drop_duplicates()   # drop_duplicates()去除重複
    df.dropna(inplace=True)  # 將空值刪除 inplace=True直接在原數據更改
    df.reset_index(inplace=True, drop=False)  # drop如果為False 則將替換的索引列添加到數據中
    print(len(df))
    print(df)

    company_person_list = []  # 要放入 公司+人名的list
    for person, company in zip(df['person_name'], df['company_name_1']):
        person_split = person.split(',')
        # print(c)
        for split_ in person_split:
            # print(s)
            company_person_str = company+' '+split_
            company_person_list.append(company_person_str)
    print(company_person_list)
    for c_i, c_obj in enumerate(company_person_list):
        search(c_i, c_obj)
        saveCsv()  # 每跑完一人名 就把網址等資料存入csv

    driver.quit()


def search(c_i, findStr):
    driver.find_element(By.CSS_SELECTOR, "input#kw").clear()
    driver.find_element(By.CSS_SELECTOR, "input#kw").send_keys(findStr)
    sleep(2)
    driver.find_element(By.CSS_SELECTOR, "input.s_btn").click()
    sleep(2)

    print("######")
    # print(findStr)
    getUrl(c_i, findStr)
    sleep(2)
    driver.find_element(By.CSS_SELECTOR, "input#kw").clear()
    sleep(2)
    # print(listLink)
    print("/////////////")


def getUrl(c_i, findStr):
    # 取得主要元素的集合
    a_elms = driver.find_elements(By.CSS_SELECTOR, 'div.imgpage ul')

    # 同時印出索引和元素 非driver也可以find_elements
    for index, elem in enumerate(a_elms):
        imgs_src = elem.find_elements(By.CSS_SELECTOR, 'div.imgbox-border img')
        imgs_list = [m.get_attribute('src') for m in imgs_src]  # 將照片網址建成list
        title_txt = elem.find_elements(By.CSS_SELECTOR, 'a')
        title_list = [t.get_attribute('title')
                      for t in title_txt]   # 將照片標題建成list
        count = 1
#         print(a1)
#         print('a11',a11)
#         print(a2)
#         print(a21)

        print("第 {} 筆".format(c_i))
        print('!!:', index)
        for imgs_i, imgs_obj in enumerate(imgs_list):
            print('??:', imgs_i)
            # 轉成字典
            if imgs_i < photolimit:
                listLink.append({
                    'name': findStr+'_'+str(imgs_i+1),   # 要存成的照片檔名
                    'link': imgs_list[imgs_i],     # 存很多照片
                    'title': title_list[count]    # 在同一個名字
                })

            else:
                break
            count += 2


def saveCsv():
    with open('Csvs/china500name_ToPhotoURL.csv', 'a', newline='', encoding='utf-8') as f:
        print("!!!!!!!!!")
        print("listLink:{}".format(listLink))

       # r = csv.writer(f)

        for index, x in enumerate(listLink):
            r = csv.DictWriter(f, fieldnames=x.keys())
            # print("$$$$$$$$")
            # print(index)
            # print(i)
            if index == 0:
                r.writeheader()
                r.writerow(x)
            else:
                r.writerow(x)


def download():
    folderPath = 'Imgs'
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    listResult = pd.read_csv(r'Csvs/china500name_ToPhotoURL.csv')
#     len(listResult)

    # 如果跑到一半斷掉 就從斷掉的地方開始
    # aa=listResult[:]
    print(len(listResult))

    for i in range(len(listResult)):
        # for i in range(len(aa)):
        print(i)
        try:
            urllib.request.urlretrieve(listResult['link'][i], os.path.join(
                folderPath, listResult['name'][i]+'.jpg'))  # listResult 變 aa
            #os.rename(os.path.join(os.path.dirname(folderPath , listResult['name'][i]+'.jpg'),os.path.pardir), listResult['name'][i]+i+'.jpg')

#             urllib.request.urlretrieve(listResult['link'][i+9916], os.path.join(folderPath , listResult['name'][i+9916]+'.jpg'))
            print(listResult['name'][i]+'.jpg 已下載')
#             print(listResult['name'][i+9916]+'.jpg 已下載')

        except urllib.error.HTTPError as exception:
            print(listResult['name'][i]+i+".jpg 無法下載")
#             print(listResult['name'][i+9916]+".jpg 無法下載")
            continue

        except TimeoutException as e:
            print(listResult['name'][i]+i+".jpg 超時")
#             print(listResult['name'][i+9916]+".jpg 超時")
            continue

        except Exception as e:
            continue

    print("done")


if __name__ == '__main__':
    visit()
    download()

print('執行完畢')
