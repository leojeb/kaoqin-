

import pandas as pd
import datetime as dt
from decimal import *
import numpy as np

# 定义两个list分别存储节假日和节日当天(计算三倍工资)
# list_dayoff = ["21-09-04", "21-09-05", "21-09-11", "21-09-12", "21-09-19", "21-09-20", "21-09-21", "21-09-25", "21-09-26"]
# list_holiday = ["21-09-21"]
#
# yuan_jilu = pd.read_excel("D:\工作\考勤\原始打卡记录20210901-20210930.xlsx")
# meir_jilu = pd.read_excel("D:\工作\考勤\安徽酷哇机器人有限公司_每日统计_20210901-20210930.xlsx")
#
# yj = yuan_jilu
# mj = meir_jilu
#
# shangban_daka_result = pd.DataFrame({
#     "姓名": yj.loc[:, "姓名"],
#     "打卡时间": yj.loc[:, "打卡时间"],
#     "打卡结果": yj.loc[:, "打卡结果"]
# })
# sb = shangban_daka_result.drop_duplicates(["姓名", "打卡时间"])
# print(sb.loc[12764,"打卡时间"].__class__.__name__)
# print(sb.to_string())
df = pd.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": np.random.randn(8),
        "D": np.random.randn(8),
    }
)
grouped = df.groupby(["A", "B"])

print(grouped.indices)
grouped.sum()
grouped.first()













