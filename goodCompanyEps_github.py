from selenium import webdriver  # 操作 browser 的 API
from selenium.common.exceptions import TimeoutException
# 面對動態網頁，等待某個元素出現的工具，通常與 exptected_conditions 搭配
from selenium.webdriver.support.ui import WebDriverWait
# 搭配 WebDriverWait 使用，對元素狀態的一種期待條件，若條件發生，則等待結束，往下一行執行
from selenium.webdriver.support import expected_conditions as EC
# 期待元素出現要透過什麼方式指定，通常與 EC、WebDriverWait 一起使用
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep  # 強制等待 (執行期間休息一下)

import pandas as pd
import numpy as np
import json  # 整理 json 使用的工具
import os
import csv
import re  # 執行 command 的時候用的

# 開始爬蟲
# 啟動瀏覽器工具的選項
options = webdriver.ChromeOptions()
# options.add_argument("--headless")              # 不開啟實體瀏覽器背景執行
options.add_argument("--start-maximized")         # 最大化視窗
options.add_argument("--incognito")               # 開啟無痕模式
options.add_argument("--disable-popup-blocking ")  # 禁用彈出攔截

# 使用 Chrome 的 WebDriver (含 options)
driver_path = Service('D:/chromedriver.exe')
driver = webdriver.Chrome(service=driver_path, options=options)
aveEpsth = ['公司名稱', '職稱', '姓名', '選任時持股', '目前持股',
            '設質股數', '設質股數佔持股比', '目前持股合計', '設質股數', '設質比例']
aveNum = len(aveEpsth)-1

# 清洗資料


def clear_datas_fn():
    # ,encoding='utf-8' 如果無法讀要先用txt轉檔
    df = pd.read_csv(r'Csvs/companyEPS.csv', encoding='utf-8')
    # https://www.796t.com/post/MjJid3M=.html
    print("info():", df.info())
    print(df)

    # 消除數字間的逗號
    df['稅後淨利'] = df['稅後淨利'].str.replace(',', '')
    print(df['稅後淨利'])

    # 將型態object轉成int64 並填空缺失值維0
    df['稅後淨利'] = pd.to_numeric(df['稅後淨利'], errors='coerce').fillna(
        '0').astype('int64')  # errors='coerce'將無效解析設置為NaN
    print(df['稅後淨利'])

    # 篩選需要的數據 有淨賺>0(單位千元)的公司
    filt = df['稅後淨利'] >= 0
    print(df.loc[filt])

    # data.loc可提取指定行數據 並印出想要的列
    df_all = df.loc[filt, ['公司代號', '公司名稱', '稅後淨利']]

    # 刪除重複欄位
    df_all = df_all.drop_duplicates(subset='公司代號')

    # 刪除缺失值
    df_all = df_all.dropna()
    print("刪除缺失值後:", len(df_all))

    df_all.to_csv('Csvs/companyEPS_new.csv', index=False)


def visit():
    global writeCount
    # 前往指定連結
    url = 'https://mops.twse.com.tw/mops/web/stapap1'
    a = 0
    writeCount = 0
    driver.get(url)
    f = open("Csvs/companyEPS_new.csv", encoding="utf8")

    readCsv = pd.read_csv(f)
    dfCsv = pd.DataFrame(readCsv)

    df_ch = dfCsv['公司代號'].values.tolist()
    df_name = dfCsv['公司名稱'].values.tolist()

    print(len(df_ch))

    for ch in df_ch:
        # 每次搜尋一家公司 爬取完並直接寫入csv
        search(ch)
        a += 1
        print(f'第{a}筆')  # 計算正在爬取第幾筆公司
        print(ch)
        downloadData(ch, df_name)
        writeCount += 1
        # print(tdContent)

        # 清空值
        driver.find_element(
            By.CSS_SELECTOR, "input[name='co_id'].textbox").clear()

        if a == len(df_ch):
            print("-------------")
            print("爬蟲結束")


def search(ch):  # search(df)

    txtInput = driver.find_element(
        By.CSS_SELECTOR, "input[name='co_id'].textbox")
    txtInput.send_keys(ch)
    sleep(3)

    btnInput = driver.find_element(
        By.CSS_SELECTOR, "div.search input[type='button']")
    btnInput.click()
    sleep(3)


def downloadData(ch, df_name):

    global th1, th2, tdContent1, tdContent2, thText, pp

    thText = ["公司名稱"]

    td1 = driver.find_elements(
        By.CSS_SELECTOR, "table.hasBorder tbody tr.odd td")  # html內基數行
    td2 = driver.find_elements(
        By.CSS_SELECTOR, "table.hasBorder tbody tr.even td")  # html內偶數行

    tdContent1 = [n.get_attribute('innerHTML').strip() for n in td1]
    tdContent2 = [n.get_attribute('innerHTML').strip() for n in td2]

    th1 = tdContent1[:aveNum]
    th2 = tdContent2[:aveNum]

    for j in thText:
        th1.insert(0, j)
        th2.insert(0, j)
        print("**************")
        print(th1)
        print(th2)
    print("*&&&&&&&&&&&&&&&&*")
    print(df_name[0])

    saveCsv(ch, df_name)


def saveCsv(ch, df_name):
    folderPath = 'Csvs'
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    with open(f"{folderPath}/company_presidents_datas.csv", 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if writeCount == 0:
            writer.writerow(aveEpsth)

        print(len(tdContent1))
        print(len(tdContent2))
        print("###############")
        print(ch)

        #
        for i in range(0, len(tdContent1), aveNum):
            # 取每行數量為標題數量 寫入csv
            c1 = tdContent1[i:i+aveNum]
            c2 = tdContent2[i:i+aveNum]

            # 因為不確定每個表格的基數偶數的行數量 所以用=0表示無此行
            if len(c1) == 0 or len(c2) == 0:
                print("沒有此行")
            else:
                # df_name是list 用索引取公司名稱
                thText = str(ch)+' '+df_name[writeCount]
                c1.insert(0, thText)   # 把公司名稱加到第一行 才能分辨下載的是那些公司
                c2.insert(0, thText)
                writer.writerow(c1)    # 每次寫入一行 直到整頁寫完
                writer.writerow(c2)

            print("((((((((()))))))))")
            print(c1)
            print(c2)

    csvfile.close()


if __name__ == '__main__':
    clear_datas_fn()
    visit()

driver.quit()
