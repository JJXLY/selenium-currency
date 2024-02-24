# 外汇牌价查询
# selenium 3.141.0
# urllib3 1.26.2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import sys


def search_name(code):
    # 查找中文货币名称
    f = open("currency_trans.txt", 'r')
    r = []
    for line in f:
        if line.split()[1] == code:
            return line.split()[0]
    return False


def isregular(date):
    leap = False  # 判断是否为闰年
    legal = False  # 判断是否合法

    # 记录 30天和 31天的月份
    month1 = {1, 3, 5, 7, 8, 10, 12}
    month2 = {4, 6, 9, 11}

    # 将输入数据按 ‘-’ 分割
    year, month, day = (int(x) for x in (date.split("-")))

    # 判断月份是否为闰年
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        leap = True
    if month in month1:
        if 1 <= day <= 31:
            legal = True
    elif month in month2:
        if 1 <= day <= 30:
            legal = True
    elif month == 2:
        if not leap and 1 <= day <= 28:
            legal = True
        elif leap and 1 <= day <= 29:
            legal = True
    return legal


# 读取日期和货币代号
# [date, code] = input().split()
[date, code] = [sys.argv[1], sys.argv[2]]
# 根据货币代号查找其对应的中文货币名称
name = search_name(code)
# 对日期进行处理
date = date[0:4] + '-' + date[4:6] + '-' + date[6:]
# 判断是否有记录该货币代号，以及日期是否合规
while not name or not isregular(date):
    if not name:
        print("The currency could not be found.")
    if not isregular(date):
        print("The date entered is irregular.")
    [date, code] = input().split()
    date = date[0:4] + '-' + date[4:6] + '-' + date[6:]
    name = search_name(code)


# 打开网页
driver = webdriver.Edge('./msedgedriver.exe')
driver.get("https://www.boc.cn/sourcedb/whpj/")
# 修改日期,找到起始时间和结束时间框，输入date
element = driver.find_element(By.ID, "historysearchform").find_elements(By.CLASS_NAME, "search_ipt")
for i in range(2):
    element[i].click()
    element[i].send_keys(Keys.BACK_SPACE)
    element[i].send_keys(date)

# 输入日期时会调动日期栏，关闭日历栏
element = driver.find_element(By.ID, "calendarPanel").find_element(By.ID, "calendarClose")
element.click()
# 选择货币
element = driver.find_element(By.ID, "historysearchform").find_element(By.ID, "pjname")
element.click()
Select(element).select_by_value(name)
# 点击搜索按键
element = driver.find_element(By.ID, "historysearchform").find_element(By.CLASS_NAME, "search_btn")
element.click()
# 爬取表格
# 定位表格，读取每一行tr
result_table = []
for i in range(10):
    table_tr_list = driver.find_element(By.CLASS_NAME, "publish").find_elements(By.TAG_NAME, "tr")
    # 记录表格数据
    table_list = []
    # 读取每一列 td,其中第一行为 th
    for tr in table_tr_list:
        if tr == table_tr_list[0]:
            tag = 'th'
        else:
            tag = 'td'
        # 获取对应数据
        table_td_list = tr.find_elements(By.TAG_NAME, tag)
        row_list = []
        for td in table_td_list:
            row_list.append(td.text)
        # 每一页的数据，以及总体数据
        table_list.append(row_list)
        result_table.append(row_list)
    # print(table_list)
    element = driver.find_element(By.CLASS_NAME, "publish").find_element(By.CLASS_NAME, "turn_next")
    element.click()

f = open("result.txt", "w")
for line in result_table:
    for each in line:
        f.write(each + ' ')
    f.write('\n')
f.close()
if result_table[1][3] == '':
    print("该货币无现汇卖出价")
else:
    print(result_table[1][3])
