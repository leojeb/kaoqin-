import pandas as pd
import datetime as dt
from decimal import *

# 定义两个list分别存储所有休息日和节日当天(计算三倍工资)
list_dayoff = ["21-10-01", "21-10-02", "21-10-03", "21-10-04", "21-10-05", "21-10-06", "21-10-07", "21-10-10",
               "21-10-16", "21-10-17"]
list_holiday = ["21-10-01", "21-10-02", "21-10-03"]

yuan_jilu = pd.read_excel("D:\工作\考勤\十月\原始记录_考勤报表_20211001-20211017(1).xlsx")
meir_jilu = pd.read_excel("D:\工作\考勤\安徽酷哇机器人有限公司_每日统计_20210901-20210930.xlsx")


yj = yuan_jilu
mj = meir_jilu
print(mj.head(100).to_string())