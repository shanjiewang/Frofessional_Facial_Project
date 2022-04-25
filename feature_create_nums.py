# 單純練習依照標準差製作假數據
from random import Random
import numpy as np
import pandas as pd
import csv
import os
import string

csv = pd.read_csv('Csvs/all_clear_rate_final.csv')
df = csv.copy()

print(df.shape)
print(df)

o_people_All = df['Label'] == 'ordinary_people'
o_people_All = df.loc[o_people_All]
o_people_All

# 非特徵類 跑亂數
o_people_Front = o_people_All[['Name', 'Sex', 'Country', 'Label']]
print(o_people_Front)

str_list = []
sex_list = []
country_list = []
label_list = []
randoms = 10000  # 要跑幾個假數據

# 隨機英文及數字組合取檔名
str10 = ''
chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
chars_len = len(chars) - 1
random = Random()

# 建立假Name
for i in range(randoms):
    str10 = ''
    for j in range(10):
        str10 += chars[random.randint(0, chars_len)]  # 從指定變數chars中建立亂數英文數字
    k = str10+'.jpg'  # 組成隨機照片名稱
    str_list.append(k)
    print(k)
print(str_list)

str_df = pd.DataFrame({'Name': str_list})


# 建立假Sex及Country
def set_list23(what_list):
    for j in range(randoms):
        k = random.randint(0, 1)
        what_list.append(int(k))
    print(what_list)


set_list23(sex_list)
set_list23(country_list)


# 新增複製ordinary_people
for i in range(randoms):
    k = 'ordinary_people'
    label_list.append(k)

sex_df = pd.DataFrame({'Sex': sex_list})
country_df = pd.DataFrame({'Country': country_list})
label_df = pd.DataFrame({'Label': label_list})

# print(str_df)
# print(sex_df)
# print(country_df)
# print(label_df)

o_people_name_df = pd.concat([str_df, sex_df, country_df, label_df],
                             axis=1, ignore_index=False)  # ignore_index:是否忽略標題
print(o_people_name_df)

# 算出普通人標準差
o_people_d = o_people_All.describe(include='all')
print(o_people_d)

start = 4
o_people_len = len(o_people_d.axes[1])   # axes[1]有幾行

# 取得標題行名稱
df_columns = o_people_d.columns.values.tolist()
df_columns = df_columns[start:]
print(df_columns)
len(df_columns)

# slice[標題列值,標題行值] 透過iloc取出標題第4至最後一行值  再透過loc取指定標題列'25%'的行值
o_people_n25 = o_people_d.iloc[:, start:o_people_len].loc['25%', ]
o_people_n75 = o_people_d.iloc[:, start:o_people_len].loc['75%', ]

o_people_list = []
o_people_feature_df = []

# 建立i組亂數 每組有j個
for i in range(randoms):
    for j in range(len(o_people_n25)):
        # 透過random.uniform取得在25%-75%間數值的每組j亂數
        k = random.uniform(o_people_n25[j], o_people_n75[j])
        k = round(k, 6)   # 取小數前6位
        o_people_list.append(k)   # 加入到陣列中
# print(ss)
# print(len(ss))

# range(起始點,ss整個list,每行放len(o_people_n25)個):
for i in range(0, len(o_people_list), len(o_people_n25)):
    k = o_people_list[i:i+len(o_people_n25)]
    o_people_feature_df.append(k)

o_people_feature_df = pd.DataFrame(o_people_feature_df)
o_people_feature_df.columns = df_columns

print(o_people_feature_df)

o_people_df = pd.concat(
    [o_people_name_df, o_people_feature_df], axis=1, ignore_index=False)
print(o_people_df)
o_people_df = o_people_df.to_csv('Csvs/o_people_df.csv')
