import datetime

import pandas as pd
import datetime as dt
from decimal import *

# 定义两个list分别存储所有休息日和节日当天(计算三倍工资)
list_dayoff = ["22-06-11", "22-06-12", "22-06-18", "22-06-19","22-06-03","22-06-04","22-06-05", "22-06-25", "22-06-26"]

list_holiday = ["22-06-03","22-06-04","22-06-05"]

dir1 = "D:\work\考勤\\202206"
yuan_jilu = pd.read_excel(f"{dir1}\安徽酷哇机器人有限公司_原始记录表_20220601-20220630.xlsx")
meir_jilu = pd.read_excel(f"{dir1}\安徽酷哇机器人有限公司_每日统计表_20220601-20220630.xlsx")


yj = yuan_jilu
mj1 = meir_jilu[meir_jilu['日期'] != '总计']

writer1 = pd.ExcelWriter(f"{dir1}\过滤考勤总表.xlsx", engine='xlsxwriter')
# writer_zhoumo = pd.ExcelWriter("D:\工作\考勤\周末出勤表(含各部门).xlsx", engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.

mj1.to_excel(writer1)
writer1.save()

mj = pd.read_excel(f"{dir1}\过滤考勤总表.xlsx")
for index, row in mj.iterrows():
    if row['日期'] == '总计':
        print('无效啊  111111111111111111111111111')

# exit()
print(yj.head(100).to_string())
# 目标result2 -> ['姓名', '考勤日期', '打卡备注', '上班1打卡时间', '上班1打卡结果', '下班1打卡时间', '下班1打卡结果', '打卡地址']
# 删除每个人日期为'总计'的那一行

# 1. 首先我们删除不需要的列
result1 = mj.loc[:, ['姓名', '部门' ,'日期', '关联的审批单']]
# result2 = yj.loc[:, ['姓名', '考勤日期', '打卡备注', '打卡时间', '打卡结果', '打卡地址']]

# 2. 把时间做个平移, 对打卡时间每一单元格数据做判断然后改变日期, 然后对打卡时间排序
yj_date = yj.loc[:, "考勤日期"]  # 加上中括号取出来的是一个dataframe, 是包含列名的, 不加中括号,取出来的是一个series, 在后面遍历的时候就可以取出每个值
yj_time = yj.loc[:, "打卡时间"]

# # 一个循环做好日期列和打卡时间列
for i in range(len(yj_time)):
    # 将打卡时间字符串拆分并得到小时数
    time_str = str(yj_time.iloc[i])
    list0 = time_str.split(" ")
    daka_date = list0[0]
    hour = int(list0[1].split(":")[0])
    minute = list0[1].split(":")[1]
    # 将考勤日期字符串转换成日期变量然后进行操作.
    date_str = str(yj_date[i])
    list1 = date_str.split(" ")
    weekday = ""
    # 直接参考打卡时间里的日期(而不用考勤日期因为钉钉太sb了), 将其变成datetime类
    date = dt.datetime.strptime(daka_date, "%Y-%m-%d")
    if hour < 5:
        # 如果打卡在凌晨五点前, 则将日期减去一天作为考勤日期
        date = date - dt.timedelta(days=1)
    # 根据日期获取当前是周几
    if (date.isoweekday() == 1):
        weekday = "星期一"
    elif (date.isoweekday() == 2):
        weekday = "星期二"
    elif (date.isoweekday() == 3):
        weekday = "星期三"
    elif (date.isoweekday() == 4):
        weekday = "星期四"
    elif (date.isoweekday() == 5):
        weekday = "星期五"
    elif (date.isoweekday() == 6):
        weekday = "星期六"
    elif (date.isoweekday() == 7):
        weekday = "星期日"

    # 全部转换成datetime对象, 方便排序和相减求工作时长
    yj_date.iloc[i] = date.strftime("%y-%m-%d") + " " + weekday
    yj_time.iloc[i] = dt.datetime.strptime(daka_date + " " + str(hour) + ":" + minute, "%Y-%m-%d %H:%M")

# 3. 按照姓名和日期分组, 求第一次打卡时间和最后一次打卡时间, 并计算工作时间
result3 = pd.DataFrame({
    "姓名": yj.loc[:, "姓名"],
    "日期": yj_date,
    "打卡时间": yj_time
}).groupby(["姓名", "日期"], as_index=False)
# print(sorted(result3.values).head[100], " 打卡时间")agg函数比较特殊, 里面的lambda里的x是groupby产生的每个list, 这里想打印是不行的
# 自定义agg模式, 我们需要对打卡时间进行判断, 如果最后一次打卡时间小于当天考勤日期的9点半, 那么就不作为下班打卡
first_daka = result3.agg(lambda x: sorted(x.values)[0])  # 第一次打卡时间,
# dayin = result3.agg(lambda x: print(sorted(x.values)))
last_daka = result3.agg(lambda x: (sorted(x.values)[len(x.values) - 1]))  # 最后一次打卡时间
# print(last_daka.to_string())
work_time = last_daka.loc[:, ["打卡时间"]] - first_daka.loc[:, ["打卡时间"]]  # 工作总时长
# print(work_time)  格式是 0 days xx:xx:xx

# 4. 用一个frames和pd.concat方法将五个列合并到一个dataframe里面
result = pd.DataFrame({
    # "姓名": first_daka.index.get_level_values("姓名"),
    # "日期": first_daka.index.get_level_values("日期"),
    "姓名": first_daka.loc[:, "姓名"],
    "日期": first_daka.loc[:, "日期"],
    "上班打卡时间": first_daka.loc[:, "打卡时间"],
    "下班打卡时间": last_daka.loc[:, "打卡时间"],
    "工作时长": work_time.loc[:, "打卡时间"]
})

# print(result.index)
# print(result.to_string())
# 5. 关联审批单
审批单 = pd.DataFrame({
    "姓名": mj.loc[:, "姓名"],
    "部门": mj.loc[:, "部门"],
    "日期": mj.loc[:, "日期"],
    "关联的审批单": mj.loc[:, "关联的审批单"],
})

shenpi = 审批单.join(result.set_index(["姓名", "日期"]), on=["姓名", "日期"])
print(shenpi.head(100).to_string())

# 6. 关联打卡结果(从原始记录里抽出打卡时间和打卡结果列)
'''
超级无敌大bug!!!!!!!
drop_duplicates()方法这里必须填 subset=["姓名","打卡时间"]
否则会有bug, 把一些本不应该去重的行给去重掉了
'''

shangban_daka_result = pd.DataFrame({
    "姓名": yj.loc[:, "姓名"],
    "打卡时间": yj.loc[:, "打卡时间"],
    "上班打卡结果": yj.loc[:, "打卡结果"]
}) \
    .drop_duplicates(subset=["姓名", "打卡时间"])

# print(shangban_daka_result.to_string())
xiaban_daka_result = pd.DataFrame({
    "姓名": yj.loc[:, "姓名"],
    "打卡时间": yj.loc[:, "打卡时间"],
    "下班打卡结果": yj.loc[:, "打卡结果"]
}).drop_duplicates(subset=["姓名", "打卡时间"])

# 　这里index为138的那一行, 李科宏在一天的同一分钟内打了两次卡, 这两次打卡记录再和上班下班打卡时间join,就把一条数据变成了四条
shangban = shenpi.join(shangban_daka_result.set_index(["姓名", "打卡时间"]), on=["姓名", "上班打卡时间"])
# print(shangban.to_string())
xiaban = shangban.join(xiaban_daka_result.set_index(["姓名", "打卡时间"]), on=["姓名", "下班打卡时间"])
# print(xiaban.to_string())
# xiaban = shangban.join(xiaban_daka_result.set_index("打卡时间"), on="下班打卡时间")
# print(xiaban.to_string())
# print(len(xiaban))

# 7. 打卡地址和打卡备注
# 抽出打卡地址和打卡时间, 姓名
sb_daka_addr = pd.DataFrame({
    "姓名": yj.loc[:, "姓名"],
    "打卡时间": yj.loc[:, "打卡时间"],
    "上班打卡地址": yj.loc[:, "打卡地址"]
}).drop_duplicates(subset=["姓名", "打卡时间"])  # drop_duplicates是因为避免有在一分钟之内打卡的记录
xb_daka_addr = pd.DataFrame({
    "姓名": yj.loc[:, "姓名"],
    "打卡时间": yj.loc[:, "打卡时间"],
    "下班打卡地址": yj.loc[:, "打卡地址"]
}).drop_duplicates(subset=["姓名", "打卡时间"])
sb_daka_note = pd.DataFrame({
    "姓名": yj.loc[:, "姓名"],
    "打卡时间": yj.loc[:, "打卡时间"],
    "上班打卡备注": yj.loc[:, "打卡备注"]
}).drop_duplicates(subset=["姓名", "打卡时间"])
xb_daka_note = pd.DataFrame({
    "姓名": yj.loc[:, "姓名"],
    "打卡时间": yj.loc[:, "打卡时间"],
    "下班打卡备注": yj.loc[:, "打卡备注"]
}).drop_duplicates(subset=["姓名", "打卡时间"])

daka_addr_result = xiaban.join(sb_daka_addr.set_index(["姓名", "打卡时间"]), on=["姓名", "上班打卡时间"]) \
    .join(xb_daka_addr.set_index(["姓名", "打卡时间"]), on=["姓名", "下班打卡时间"])
# print(daka_addr_result.to_string())
daka_note_result = daka_addr_result.join(sb_daka_note.set_index(["姓名", "打卡时间"]), on=["姓名", "上班打卡时间"]) \
    .join(xb_daka_note.set_index(["姓名", "打卡时间"]), on=["姓名", "下班打卡时间"])
print(daka_note_result.head(200).to_string())


# 8. 剩下几个列 :  有无加班补贴, 有无周末加班费
list_jiaban = []
list_zhoumo = []
list_jiaban_T = []
# print(shenpi.to_string()) # 用其他的表求len的时候会有问题, 最好以shenpi或者审批表变量的长度为准
# print(daka_note_result.to_string())
# print(daka_note_result.loc[138, "工作时长"].to_string())
# print(str(daka_note_result.loc[2549, "下班打卡时间"]) == "NaT")

# 获取一些后面要用的量
wudian = dt.timedelta(hours=5)
zao = dt.timedelta(hours=9, minutes=30)
lunch_start = dt.timedelta(hours=12)
lunch_end = dt.timedelta(hours=13)
wan = dt.timedelta(hours=18, minutes=30)
dinner_start = dt.timedelta(hours=18, minutes=30)
dinner_end = dt.timedelta(hours=19, minutes=30)

# 更改上下班相关列, 并生成是否计算加班费和周末加班费的list
print(daka_note_result.columns.tolist())
# print(daka_note_result.loc[0, '日期'])
for i, rows in daka_note_result.iterrows():
    # print(11111111111111111111111111, daka_note_result.iloc[i, "日期"])
    riqi = str(daka_note_result.loc[i, "日期"])
    datestr = riqi.split(" ")[0]
    try:
        date = dt.datetime.strptime(datestr, "%y-%m-%d")
    except Exception:
        print(datestr, "     ", riqi )
        print(i,"是异常行")

    shenpistr = str(daka_note_result.loc[i, "关联的审批单"])
    workT_str = str(daka_note_result.loc[i, "工作时长"])
    # 主条件是判断工作时长是否为空, 次级条件是判断是否是休息日, 可能还需判断是否是节假日当天
    if workT_str != "NaT":
        # 定义一些用到的变量
        sbHour = str(daka_note_result.loc[i, "上班打卡时间"]).split(" ")[1].split(":")[0]
        sbMin = str(daka_note_result.loc[i, "上班打卡时间"]).split(" ")[1].split(":")[1]
        sbT = dt.timedelta(hours=int(sbHour), minutes=int(sbMin))

        xbHour = str(daka_note_result.loc[i, "下班打卡时间"]).split(" ")[1].split(":")[0]
        xbMin = str(daka_note_result.loc[i, "下班打卡时间"]).split(" ")[1].split(":")[1]
        xbT = dt.timedelta(hours=int(xbHour), minutes=int(xbMin))

        time1 = workT_str.split(" ")[2]
        T = time1.split(":")
        # 1. 把工作时长用小数表示
        work_time1 = int(T[0]) + int(T[1]) / 60.00
        work_time_formatted = Decimal(work_time1).quantize(Decimal("0.00"))
        daka_note_result.loc[i, "工作时长"] = work_time_formatted

        if datestr in list_dayoff:
            # 如果是休息日, 普通加班费列为空
            list_jiaban.append("")
            # 判断是否计算周末加班费, 以及是否为节假日当天(三倍工资)
            if time1 == "00:00:00":
                # 工作时长为0, 无周末加班费
                list_zhoumo.append("")
                list_jiaban_T.append(0.00)
                # 同时判断这次打卡是上班还是下班, 然后把另外一个打卡的记录改动一下
                # 因为是5点到5点, 所以这里判断还不能这么做;
                if wudian < sbT < zao:
                    daka_note_result.loc[i, "下班打卡时间"] = ""
                    daka_note_result.loc[i, "下班打卡结果"] = "缺卡"
                    daka_note_result.loc[i, "下班打卡地址"] = ""
                elif sbT < wudian or sbT > wan:
                    daka_note_result.loc[i, "上班打卡时间"] = ""
                    daka_note_result.loc[i, "上班打卡结果"] = "缺卡"
                    daka_note_result.loc[i, "上班打卡地址"] = ""
                else:
                    if sbT - zao > wan - sbT:
                        daka_note_result.loc[i, "上班打卡时间"] = ""
                        daka_note_result.loc[i, "上班打卡结果"] = "缺卡"
                        daka_note_result.loc[i, "上班打卡地址"] = ""
                    else:
                        daka_note_result.loc[i, "下班打卡时间"] = ""
                        daka_note_result.loc[i, "下班打卡结果"] = "缺卡"
                        daka_note_result.loc[i, "下班打卡地址"] = ""
            else:  # 工作时长不为0
                # 需要计算是否为节假日当天
                jiaban_T = 0.00
                if sbT < lunch_start:
                    if xbT <= lunch_start:
                        jiaban_T = work_time1
                    elif lunch_start < xbT < lunch_end:
                        jiaban_T = work_time1 - (xbT - lunch_start).total_seconds()/3600
                    elif xbT >= lunch_end:
                        jiaban_T = work_time1 - 1

                elif lunch_start <= sbT < lunch_end:
                    if xbT < lunch_end:
                        jiaban_T = 0.00
                    elif dinner_start > xbT >= lunch_end:
                        jiaban_T = work_time1 - (lunch_end - sbT).total_seconds()/3600
                    elif xbT >= dinner_start:
                        if ((xbT - dinner_start) + (lunch_end - sbT)) > datetime.timedelta(hours=1):
                            jiaban_T = work_time1 - 1
                        else:
                            jiaban_T = work_time1 - ((xbT - dinner_start) + (lunch_end - sbT)).total_seconds()/3600
                elif lunch_end <= sbT < dinner_start:
                    if xbT < dinner_start:
                        jiaban_T = work_time1
                    elif dinner_start <= xbT < dinner_end:
                        jiaban_T = work_time1 - (xbT - dinner_start).total_seconds()/3600
                    elif dinner_end <= xbT:
                        jiaban_T = work_time1 - 1
                elif dinner_start <= sbT < dinner_end:
                    if xbT < dinner_end:
                        jiaban_T = 0
                    else:
                        jiaban_T = work_time1 - (dinner_end - sbT).total_seconds()/3600
                elif sbT >= dinner_end:
                    jiaban_T = work_time1

                jiaban_T_formatted = Decimal(jiaban_T).quantize(Decimal("0.00"))
                list_jiaban_T.append(jiaban_T_formatted)

                if datestr in list_holiday:
                    list_zhoumo.append("法定节日当天")
                else:
                    list_zhoumo.append("是")

        else:
            # 如果不是休息日, 周末加班费无, 判断是否计算加班费
            list_zhoumo.append("")

            # 如果工作时长是0, 表明当天只打了一次, 再判断这次时间离上下班哪个进, 然后改该条记录(周末工作日都如此)
            if time1 == "00:00:00":
                # 因为是5点到5点, 所以这里判断还不能这么做;
                if wudian < sbT < zao:
                    daka_note_result.loc[i, "下班打卡时间"] = ""
                    daka_note_result.loc[i, "下班打卡结果"] = "缺卡"
                    daka_note_result.loc[i, "下班打卡地址"] = ""
                elif sbT < wudian or sbT > wan:
                    daka_note_result.loc[i, "上班打卡时间"] = ""
                    daka_note_result.loc[i, "上班打卡结果"] = "缺卡"
                    daka_note_result.loc[i, "上班打卡地址"] = ""
                else:
                    if sbT - zao > wan - sbT:
                        daka_note_result.loc[i, "上班打卡时间"] = ""
                        daka_note_result.loc[i, "上班打卡结果"] = "缺卡"
                        daka_note_result.loc[i, "上班打卡地址"] = ""
                    else:
                        daka_note_result.loc[i, "下班打卡时间"] = ""
                        daka_note_result.loc[i, "下班打卡结果"] = "缺卡"
                        daka_note_result.loc[i, "下班打卡地址"] = ""
                list_jiaban.append("")
                list_jiaban_T.append(0.00)
            elif work_time1 >= 11.50:
                list_jiaban.append("是")

                list_jiaban_T.append(Decimal(work_time1 - 9.00).quantize(Decimal("0.00")))
            else:
                list_jiaban.append("")
                list_jiaban_T.append(Decimal(work_time1 - 9.00).quantize(Decimal("0.00")))

        # 2. 打卡时间全部改成只有小时数
        sbT1 = daka_note_result.loc[i, "上班打卡时间"]
        xbT1 = daka_note_result.loc[i, "下班打卡时间"]
        if sbT1 != "" and sbT1 != "NaT":  # 这里不需要判断时间是NaT, 因为大if已经判断了workT不是NaT了, 那么上下班肯定也不是NaT
            daka_note_result.loc[i, "上班打卡时间"] = str(sbT1).split(" ")[1]
        if xbT1 != "" and xbT1 != "NaT":
            daka_note_result.loc[i, "下班打卡时间"] = str(xbT1).split(" ")[1]

    else:
        # workT为空
        # 非周末, 那么改成缺卡, 且没有加班费, 如果是周末则不作任何操作
        if datestr not in list_dayoff:
            daka_note_result.loc[i, "上班打卡结果"] = "缺卡"
            daka_note_result.loc[i, "下班打卡结果"] = "缺卡"
        # 加班费和周末加班费都填一个空, 因为根本没打卡
        list_jiaban.append("")
        list_zhoumo.append("")
        list_jiaban_T.append(0.00)

    # 有一个需求, 如果审批单里面有请假的, 把后面对应的打卡变成请假
    if '假' in shenpistr:
        if '08:30' in shenpistr or '09:30' in shenpistr:
            daka_note_result.loc[i, "上班打卡结果"] = "请假"
        if '17:30' in shenpistr or '18:30' in shenpistr:
            daka_note_result.loc[i, "下班打卡结果"] = "请假"

    if '调休' in shenpistr:
        if '08:30' in shenpistr or '09:30' in shenpistr:
            daka_note_result.loc[i, "上班打卡结果"] = "调休"
        if '17:30' in shenpistr or '18:30' in shenpistr:
            daka_note_result.loc[i, "下班打卡结果"] = "调休"


# 将做好的两个list 转换成 Series, 然后合并到打卡备注表上面
s1_jiaban = pd.Series(list_jiaban, name="是否计算加班补贴")
s2_zhoumo = pd.Series(list_zhoumo, name="是否计算周末加班费")
s3_jiaban_T = pd.Series(list_jiaban_T, name="加班时长")
print(len(s1_jiaban), "-----加班")
print(len(s2_zhoumo), "-----周末")
final_result = pd.concat([daka_note_result, s3_jiaban_T, s1_jiaban, s2_zhoumo], axis=1)
# print(final_result.to_string())
# print(len(final_result))

# 从final_result获取出勤表, 要求(需要每两周把大家周末有出勤的考勤数据都拉出来（分部门），给各部门负责人核对一下加班情况)
# dept = mj.loc[:, ["姓名", "部门"]].drop_duplicates("姓名")  # 姓名,部门表
# # print(dept.to_string())
# dept_include = final_result.join(dept.set_index("姓名"), on="姓名")


# print(dept_include)


# 需求a. 定义函数来筛选节假日出勤的行(节假日当天需要注明)

def keeprow(df):
    list_boolean = []
    riqi = df["日期"]

    for i, row in df.iterrows():
        # print(i, type(riqi.loc[i]), riqi.loc[i])

        datastr = ''
        if '星期' in str(riqi.loc[i]):
            datestr = riqi.loc[i].split(" ")[0]
        else:
            print(False, '-----------------')
            list_boolean.append(False)
            continue
        # date = dt.datetime.strptime(datestr, "%y-%m-%d")
        boolean = (str(df['工作时长'].loc[i]) != "NaT") and (datestr in list_dayoff)
        list_boolean.append(boolean)
    return list_boolean


weekend_work = final_result.loc[keeprow(final_result)]

# 最后改一下表的每列的顺序
formatted_kaoqin = pd.DataFrame({
    "姓名": final_result["姓名"],
    "日期": final_result["日期"],
    "部门": final_result["部门"],
    "工作时长(小时)": final_result["工作时长"],
    "关联的审批单": final_result["关联的审批单"],
    "上班打卡时间": final_result["上班打卡时间"],
    "上班打卡结果": final_result["上班打卡结果"],
    "上班打卡地址": final_result["上班打卡地址"],
    "下班打卡时间": final_result["下班打卡时间"],
    "下班打卡结果": final_result["下班打卡结果"],
    "下班打卡地址": final_result["下班打卡地址"],
    "上班打卡备注": final_result["上班打卡备注"],
    "下班打卡备注": final_result["下班打卡备注"],
    "加班时长(小时)": final_result["加班时长"],
    "是否计算加班补贴": final_result["是否计算加班补贴"],
    "是否计算周末加班费": final_result["是否计算周末加班费"]
})


formatted_weekend = pd.DataFrame({
    # "部门": weekend_work["部门"],
    "姓名": weekend_work.loc[:, "姓名"],
    "日期": weekend_work.loc[:, "日期"],
    "部门": weekend_work.loc[:, "部门"],
    "工作时长(小时)": weekend_work.loc[:, "工作时长"],
    "关联的审批单": weekend_work.loc[:, "关联的审批单"],
    "上班打卡时间": weekend_work.loc[:, "上班打卡时间"],
    "上班打卡结果": weekend_work.loc[:, "上班打卡结果"],
    "上班打卡地址": weekend_work.loc[:, "上班打卡地址"],
    "下班打卡时间": weekend_work.loc[:, "下班打卡时间"],
    "下班打卡结果": weekend_work.loc[:, "下班打卡结果"],
    "下班打卡地址": weekend_work.loc[:, "下班打卡地址"],
    "上班打卡备注": weekend_work.loc[:, "上班打卡备注"],
    "下班打卡备注": weekend_work.loc[:, "下班打卡备注"],
    "加班时长(小时)": weekend_work.loc[:, "加班时长"],
    "是否计算加班补贴": weekend_work.loc[:, "是否计算加班补贴"],
    "是否计算周末加班费": weekend_work.loc[:, "是否计算周末加班费"],
    # 这里weekend的index是过滤后的不连续的index, 我们改成range(len(weekend_work))从0开始
})

print(len(weekend_work))
# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(f"{dir1}\考勤总表.xlsx", engine='xlsxwriter')
# writer_zhoumo = pd.ExcelWriter("D:\工作\考勤\周末出勤表(含各部门).xlsx", engine='xlsxwriter')
# Convert the dataframe to an XlsxWriter Excel object.

formatted_kaoqin.to_excel(writer, sheet_name='考勤表')
formatted_weekend.to_excel(writer, sheet_name='休息日出勤总表')
# weekend_groupby_dept = formatted_weekend.groupby(['部门'], as_index=False)
# 按照部门分组后输出为不同的excel表格,
# for name, group in weekend_groupby_dept:
#     group.to_excel(writer_zhoumo, sheet_name=str(name))
# Get the xlsxwriter workbook and worksheet objects.
workbook = writer.book

# 定义格式, 有几种情况, 每种都用不同的颜色
format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
format1 = workbook.add_format({'align': 'left', 'valign': 'vcenter'})
format_biaoti = workbook.add_format(
    {'bg_color': '#FFFFCC', 'border': 1, 'border_color': '#D4D4D4', 'align': 'center', 'valign': 'vcenter'})
cell_format1 = workbook.add_format(
    {'bg_color': 'yellow', 'border': 1, 'border_color': '#D4D4D4', 'align': 'center', 'valign': 'vcenter'})  # 缺卡格式
cell_format2 = workbook.add_format(
    {'bg_color': '#FFCC99', 'border': 1, 'border_color': '#D4D4D4', 'align': 'center',
     'valign': 'vcenter'})  # 补卡审批, 单元格标青色
cell_format3 = workbook.add_format(
    {'bg_color': 'cyan', 'border': 1, 'border_color': '#D4D4D4', 'align': 'center', 'valign': 'vcenter'})  # 迟到, 单元格标蓝
cell_format4 = workbook.add_format(
    {'bg_color': '#FFCC99', 'border': 1, 'border_color': '#D4D4D4', 'align': 'center', 'valign': 'vcenter'})  # 请假, 表棕色
# cell_format5 = workbook.add_format({'bg_color': '#F8C8C8', 'border': 1, 'border_color': '#D4D4D4'}) # 出差 标此色
cell_format6 = workbook.add_format(
    {'bg_color': '#DFF1AB', 'border': 1, 'border_color': '#D4D4D4', 'align': 'center', 'valign': 'vcenter'})  # 外勤 标此色

worksheet = writer.sheets['考勤表']
worksheet1 = writer.sheets['休息日出勤总表']
# 设置两个表的格式
worksheet.set_row(0, 20, format_biaoti)
worksheet1.set_row(0, 20, format_biaoti)
for i, row in formatted_kaoqin.iterrows():
    worksheet.set_row(i + 1, 35, format)  # 设置行高和居中
    sb_daka_res = formatted_kaoqin.loc[i, "上班打卡结果"]
    xb_daka_res = formatted_kaoqin.loc[i, "下班打卡结果"]
    shenpidan = str(formatted_kaoqin.loc[i, "关联的审批单"])
    # 如果有缺卡, 该行显示为黄色
    if sb_daka_res == "缺卡" or xb_daka_res == "缺卡":
        worksheet.set_row(i + 1, 35, cell_format1)
    # 补卡审批, 单元格标绿
    if "补卡" in shenpidan:
        worksheet.write(i + 1, 4, shenpidan, cell_format2)
    if sb_daka_res == "补卡审批通过":
        worksheet.write(i + 1, 6, sb_daka_res, cell_format2)
    if xb_daka_res == "补卡审批通过":
        worksheet.write(i + 1, 9, xb_daka_res, cell_format2)
    # 迟到单元格标蓝
    if sb_daka_res == "迟到":
        worksheet.write(i + 1, 6, sb_daka_res, cell_format3)
    if xb_daka_res == "迟到":
        worksheet.write(i + 1, 9, xb_daka_res, cell_format3)
    # 请假, 标棕色
    if "假" in shenpidan:
        worksheet.write(i + 1, 4, shenpidan, cell_format4)
    if sb_daka_res == "请假" or sb_daka_res == "调休":
        worksheet.write(i + 1, 6, sb_daka_res, cell_format4)
    if xb_daka_res == "请假" or xb_daka_res == "调休":
        worksheet.write(i + 1, 9, xb_daka_res, cell_format4)
    if sb_daka_res == "外勤":
        worksheet.write(i + 1, 6, sb_daka_res, cell_format6)
    if xb_daka_res == "外勤":
        worksheet.write(i + 1, 9, xb_daka_res, cell_format6)
    # worksheet1.write(index1, 4, shenpidan, format1) 会完全覆盖, 所以颜色也会消失..那就算了把
# print(formatted_weekend.loc[10, "上班打卡结果"],formatted_weekend.loc[10, "上班打卡结果"].__class__.__name__)

list_index = formatted_weekend.index.tolist()
for j in list_index:
    index1 = list_index.index(j) + 1
    worksheet1.set_row(index1, 35, format)
    sb_daka_res = formatted_weekend.loc[j, "上班打卡结果"]
    xb_daka_res = formatted_weekend.loc[j, "下班打卡结果"]
    shenpidan = str(formatted_weekend.loc[j, "关联的审批单"])
    # 如果有缺卡, 该行显示为黄色
    if sb_daka_res == "缺卡" or xb_daka_res == "缺卡":
        worksheet1.set_row(index1, 35, cell_format1)
    # 补卡审批, 单元格标绿
    if "补卡" in shenpidan:
        worksheet1.write(index1, 4, shenpidan, cell_format2)
    if sb_daka_res == "补卡审批通过":
        worksheet1.write(index1, 6, sb_daka_res, cell_format2)
    if xb_daka_res == "补卡审批通过":
        worksheet1.write(index1, 9, xb_daka_res, cell_format2)
    # 迟到单元格标蓝
    if sb_daka_res == "迟到":
        worksheet1.write(index1, 6, sb_daka_res, cell_format3)
    if xb_daka_res == "迟到":
        worksheet1.write(index1, 9, xb_daka_res, cell_format3)
    # 请假, 标棕色
    if "假" in shenpidan:
        worksheet1.write(index1, 4, shenpidan, cell_format4)
    if sb_daka_res == "请假" or sb_daka_res == "调休":
        worksheet1.write(index1, 6, sb_daka_res, cell_format4)
    if xb_daka_res == "请假" or xb_daka_res == "调休":
        worksheet1.write(index1, 9, xb_daka_res, cell_format4)
    if sb_daka_res == "外勤":
        worksheet1.write(index1, 6, sb_daka_res, cell_format6)
    if xb_daka_res == "外勤":
        worksheet1.write(index1, 9, xb_daka_res, cell_format6)

# Note: It isn't possible to format any cyj.loc[i, ["姓名e, "部门lls that already have a format such
# as the index or headers or any cells that contain dates or datetimes.

# Set the column width and format.

worksheet.set_column('E:O', 18, None)
worksheet.set_column('B:B', 12, None)
worksheet.set_column('C:C', 18, None)
worksheet.set_column('D:D', 15, None)

worksheet1.set_column('E:P', 18, None)
worksheet1.set_column('B:B', 8, None)
worksheet1.set_column('C:C', 18, None)
worksheet1.set_column('D:D', 15, None)

# Close the Pandas Excel writer and output the Excel file.
writer.save()
# writer_zhoumo.save()
