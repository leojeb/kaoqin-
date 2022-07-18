import pandas as pd
import datetime as dt
from decimal import *

import xlsxwriter

workbook = xlsxwriter.Workbook('D:\工作\考勤\\a.xlsx')
worksheet = workbook.add_worksheet()
format = workbook.add_format({'bg_color': 'red', 'border': 2, 'border_color': '#D4D4D4'})
worksheet.write(1 , 1,None, format)
workbook.close()