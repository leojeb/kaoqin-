# coding=utf-8
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import calendar
import pandas

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(__name__)
    print_hi('PyCharm')

raw_input("请输入一个值,\n")
# while 1 == 1:
#     print()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# 可写函数说明
def printinfo(arg1, *vartuple):
    "打印任何传入的参数"
    print "输出: "
    print arg1
    for var in vartuple:
        print var, " ",
    return


# 调用printinfo 函数
printinfo(10)
printinfo(70, 60, 50)

dict1 = globals()
print dict1.keys()
