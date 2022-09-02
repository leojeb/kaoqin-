import datetime

import pandas as pd
import datetime as dt
from datetime import timedelta
from decimal import *



pdframe = pd.read_excel("C:\\Users\\leon\\Documents\\WeChat Files\\wxid_40bwl7m3jqaj22\\FileStorage\\File\\2022-08\\cm_for_compete.xlsx")
print(pdframe['id06'].head(100).to_string())

# 1.1
ques1_1 = pdframe[[ele != '9d5ed6' or ele != 'b9ece1' for ele in list(pdframe['id06'])]]
print(ques1_1.head(100).to_string())

#1.2
# scope复制到这里
scope = """aaaa/bbbbb/dfgfgd/bdafg/badfga"""
scope_list = scope.split('/')
pre_ques1_2 = ques1_1[[ele != '9d5ed6' for ele in list(ques1_1['id06'])]]
ques1_2 = pre_ques1_2[[ele not in scope_list for ele in list(pre_ques1_2['id07'])]]

print(ques1_2.head(100).to_string())

#1.3
pre_ques1_3 = ques1_2[[ele != '5dbc98'  for ele in list(ques1_2['id06'])]]
ques1_3: pd.DataFrame = pre_ques1_3[[ele not in scope_list for ele in list(pre_ques1_3['id08'])]]

print(ques1_3.head(100).to_string())
#1.4
print(len(ques1_3['id06']), ques1_3.columns.__len__())



#2.1
for i, rows in ques1_3.iterrows():
    for ele in rows:
        if not ele:
            ques1_3.drop(index=i)

print(ques1_3.head(100).to_string())

#2.2
print(ques1_3.columns.tolist())
ques2_2 = ques1_3
for i in ques2_2.columns.tolist():
    first_ele = ques2_2[i][0]
    flag = True
    for ele in ques2_2[i]:
        if ele != first_ele:
            flag = False
            break

    if flag:
        del ques2_2[i]


print(ques2_2.head(100).to_string())

#2.3
print(len(ques2_2[ques2_2.columns.tolist()[0]]), ques2_2.columns.__len__())

#3.1
ques3_1_grouped = ques1_3.groupby(['id03','id04','id05'])
print(ques3_1_grouped.groups.items())
counts = []
index_name = []
for i in ques3_1_grouped.groups.items():
    print(len(i))
    counts.append(len(i[1]))
    index_name.append(i[0])

df1 = pd.DataFrame(data={'counts':counts, "index": index_name})

df1['rank'] = df1['counts'].rank(ascending=False)
print(df1)

print(f"请输入一个整数, 范围在0到{len(df1['rank'])}之间")
T = input()
row_choice = df1[[int(ele) == T for ele in df1['rank']]]
print(row_choice)
print(row_choice['index'], row_choice['counts'])

