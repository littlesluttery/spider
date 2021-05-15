#-*- coding=utf-8 -*-
#@Time : 2020/10/8 1:11 PM
#@Author : 小邋遢
#@File : intellectual_cookies.py
#@Software : PyCharm
import random
import re
import time

import pymysql
import pytesseract
from intellectual_property.config import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import cv2
import pandas as pd

import pytesseract
from PIL import Image, ImageDraw

class Intellectual_Cookies():
    def __init__(self):
        self.url = START_URL
        self.config = CONFIG

    def coonect_mysql(self):
        db = pymysql.connect(**self.config)
        cursor = db.cursor()
        return db, cursor

    def run(self):

        # 模拟登录，拿到cookies
        cookies = self.login(self.url)
        print(cookies)
        #cookie_1 = cookies[0]['value']
        #cookies = "JSESSIONID=" + cookie_1 + " " + "IS_LOGIN=true;" + " " + ";avoid_declare=declare_pass"
        # 将cookies保存到数据库
        db,cursor = self.coonect_mysql()
        sql = 'update cookies set cookies="{}" where id=1'.format(cookies)
        cursor.execute(sql)
        db.commit()


    def parse_code(self,driver):

        # 保存网页完整图片
        driver.save_screenshot('code.png')

        # 将照片大小确定在1600*1200大小
        image = Image.open('code.png')
        image_resize = image.resize((1600, 1200), Image.ANTIALIAS)
        image_resize.save("code.png")

        # 裁剪图片
        img = cv2.imread('code.png')
        #cro = img[1040:1100, 1400:1560] # 无头浏览器的截取范围
        cro = img[1040:1106, 2282:2397]  # 非无头浏览器截取范围
        cv2.imwrite('real_code.png', cro)

        # 清洁图片
        # 打开图片
        image = Image.open("real_code.png")
        # 将图片转换成灰度图片
        image = image.convert("L")
        # 去噪,G = 50,N = 4,Z = 4
        self.clearNoise(image, 50, 4, 4)
        # 保存图片
        image.save("real_code.png")

        # 识别验证码
        text = pytesseract.image_to_string("real_code.png")
        print(text)
        return text


    def login(self,url):
        # 随机选择一个账户进行登录
        x = random.choice([1,2])
        print(x)
        db,cursor = self.coonect_mysql()
        sql = 'select * from user_table where id={}'.format(3)
        data_user = pd.read_sql_query(sql,db)
        username = data_user['username'][0]
        password = data_user['password'][0]
        print(username)
        options = webdriver.ChromeOptions()

        options.add_argument('--headless')
        #driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome()
        driver.maximize_window()

        wait = WebDriverWait(driver, 10)
        print("正在登录专利检索系统.......")
        driver.get(url)

        username_ele = wait.until(EC.presence_of_element_located((By.ID, 'j_username')))
        password_ele = wait.until(EC.presence_of_element_located((By.ID, 'j_password_show')))
        code = wait.until(EC.presence_of_element_located((By.ID, 'j_validation_code')))
        time.sleep(2)
        username_ele.send_keys(username)
        time.sleep(2)
        password_ele.send_keys(password)
        time.sleep(3)
        print("等待......")

        text = self.parse_code(driver)

        time.sleep(10)
        code.send_keys(text)
        time.sleep(3)
        #driver.find_element_by_xpath("//div[@class='modular_unlogin-btn']/a[1]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//li[@class='menuLI'][1]/a").click()
        time.sleep(3)

        time.sleep(3)
        driver.find_element_by_xpath("//input[@id='search_input']").send_keys("沈阳九日实业有限公司")

        time.sleep(7)
        driver.find_element_by_xpath("//a[@id='btn_generalSearch']").click()

        data = driver.get_cookies()
        print(data)
        cookies= []
        for i in data:
            name = i['name']
            value = i['value']
            cookies.append("{}={}; ".format(name,value))

        cookies = ''.join(cookies)
        driver.close()
        return cookies



    # 二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
    # 该函数也可以改成RGB判断的,具体看需求如何
    def getPixel(self,image, x, y, G, N):
        L = image.getpixel((x, y))
        if L > G:
            L = True
        else:
            L = False

        nearDots = 0
        if L == (image.getpixel((x - 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y + 1)) > G):
            nearDots += 1

        if nearDots < N:
            return image.getpixel((x, y - 1))
        else:
            return None

    # 降噪
    # 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
    # G: Integer 图像二值化阀值
    # N: Integer 降噪率 0 <N <8
    # Z: Integer 降噪次数
    # 输出
    #  0：降噪成功
    #  1：降噪失败
    def clearNoise(self,image, G, N, Z):
        draw = ImageDraw.Draw(image)

        for i in range(0, Z):
            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    color = self.getPixel(image, x, y, G, N)
                    if color != None:
                        draw.point((x, y), color)


if __name__ == '__main__':
    ic = Intellectual_Cookies()
    ic.run()