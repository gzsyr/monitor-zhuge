import os
import time
from asyncore import write

import pytest
import xlrd
from selenium import webdriver
from selenium.webdriver.common.by import By

# WORKSPACE_DIR = os.path.abspath(os.getcwd())

PATH = r'C:\Users\Administrator\Downloads'
FILE = '事件_事件概览.xlsx'

class ActionTest:
    def __init__(self):
        self.option = webdriver.ChromeOptions()

        self.option.add_experimental_option('detach', True)
        # self.option.add_experimental_option('download.default_directory', FILE_DIR)
        self.chromedriver_path = r"C:\Users\Administrator\monitor-zhuge\zhuge\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path, options=self.option)
        self.driver.maximize_window()

    def open_url(self, url):
        self.driver.get(url)

    def login(self):
        # 登录
        self.driver.find_element(By.CSS_SELECTOR, "[type=text]").send_keys('13776601230')
        self.driver.find_element(By.CSS_SELECTOR, "[type=password]").send_keys('hym0206!')
        self.driver.find_element(By.TAG_NAME, "button").click()

    def gggj(self):
        # 点击365广告工具
        self.driver.find_element(By.CLASS_NAME, 'zg-select-arrow').click()
        time.sleep(2)
        # 点击淘房365（正式）
        # self.driver.find_element(By.XPATH, '//*[@id="layout"]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[2]/div[1]/li[2]/span/div/span').click()
        self.driver.find_element(By.XPATH, "//*[text()='淘房365(正式)']").click()
        # e = self.driver.find_elements(By.CLASS_NAME, "app-drop-option")
        # for i in e:
        #     t = i.find_element(By.TAG_NAME, 'span')
        #     if '淘房365(正式)' in t.text:
        #         t.click()
        #         break

    def fenxi(self):
        # 点击分析
        self.driver.find_element(By.XPATH, '//*[@id="layout"]/div[2]/div/div/div[2]/div[2]/span[1]').click()
        time.sleep(2)
        # 点击事件
        self.driver.find_elements(By.CLASS_NAME, "analysis-page-desc")[1].click()

    def derive(self):
        # 导出
        self.driver.find_element(By.CLASS_NAME, 'icon-download').click()

    def close_driver(self):
        # 关闭浏览器
        self.driver.quit()

    def updatefile(self):
        old_name = PATH + '/' + FILE   # 'RESULTS.CSV'这个文件原来的名字
        new = PATH + '/' + 'zhuge_' + time.strftime('%Y-%m-%d') + '.xlsx'  # 改为这个新名字
        os.rename(old_name, new)

def excel():
    action = ActionTest()
    action.open_url("https://cdp.365sydc.com/")
    time.sleep(2)
    action.login()
    time.sleep(3)
    action.gggj()
    time.sleep(2)
    action.fenxi()
    time.sleep(3)
    action.derive()
    time.sleep(3)
    action.close_driver()

    file_test = xlrd.open_workbook(PATH + '/' + FILE)  # 读取事件_事件概览.xlsx文件
    count = len(file_test.sheets())
    # 获取该文件中的工作簿数
    print("工作簿总数为：", count)
    table1 = file_test.sheet_by_name("sheet")
    # 根据工作簿名字获取该工作簿的数据
    nrows = table1.nrows
    # 获取工作簿行数
    ncols = table1.ncols
    # 获取工作簿列数
    print("Sheet的行数为：", nrows, "列数为：", ncols)
    # 从第二行开始，遍历Sheet中的数据（第一行为表头）
    list_data = []
    case = []
    title = []
    title.append(table1.row_values(0)[0] + ' ')
    title.append(table1.row_values(0)[1])
    title.append(table1.row_values(0)[7])
    title.append('下降率')
    for i in range(1, nrows):
        # 按行读取数据
        rowvalues = table1.row_values(i)
        # 第一列为序号，取第二列
        # 事件名
        key1 = rowvalues[0]
        # 第七天的数据
        key2 = rowvalues[1]
        # 第二天的数据
        key3 = rowvalues[7]
        # 值
        if key2 == 0:
            # print(key1, "----------", key2, "----------", key3, "----------", "被除数为0")
            continue
        key4 = (key3 - key2) / key2 * 100
        # table.write(0, rowvalues[8], key4)

        ldata = []
        if (key3-key2) <= -10 and key4 <= -50:
            print(key1, "----------", key2, "----------", key3, "----------", key4)
            ldata.append(key1)
            ldata.append(key2)
            ldata.append(key3)
            ldata.append(key4)
            # print(ldata)
            list_data.append(ldata)
    action.updatefile()
    # 排序
    list_data.sort(key=lambda tup: tup[3])

    note = open('zg-' + time.strftime('%Y-%m-%d') + '.txt', encoding='utf-8', mode='a+')
    # note.write(','.join(title) + '\n')

    t1 = '%s|%10s|%10s|  %s' % (title[0].ljust(20, '　'), title[1], title[2], title[3])
    note.write(t1 + '\n')

    for i in list_data:
        case.append(i[0])

        # lst = list(map(lambda x: str(x), i))
        # str1 = ','.join(lst)
        str1 = '%s|%10d|%10d|  %.2f' % (i[0].ljust(20, '　'), i[1], i[2], i[3])
        note.write(str1 + '\n')

    note.close()

    params = zip(case, list_data)
    return case, params


case, params = excel()
list_params = list(params)

@pytest.mark.parametrize("case, value", list(list_params), ids=case)
def test_(case, value):
    assert True==False

