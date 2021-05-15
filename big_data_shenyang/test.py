#-*- coding=utf-8 -*-
#@Time : 2020/9/28 5:17 PM
#@Author : 秦龙
#@File : test.py
#@Software : PyCharm
"""
import requests,time
from selenium import webdriver
from lxml import etree

url = "http://218.60.146.4/pubsearch/portal/uiIndex.shtml"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(2)
driver.find_element_by_id("j_username").send_keys("DBKJDSC2020")
time.sleep(2)
driver.find_element_by_id("j_password_show").send_keys("DBKJDSC2020")
time.sleep(10)



url = "http://218.60.146.4/pubsearch/patentsearch/searchHomeIndex-searchHomeIndex.shtml"
driver.get(url)
time.sleep(2)

driver.find_element_by_id("search_input").send_keys("辽宁航安特铸材料有限公司")
#driver.find_element_by_xpath("//input[@id='search_input']").send_keys("西安邮电大学")
#driver.find_element_by_id("search_input").send_keys("西安邮电大学")
driver.find_element_by_id("btn_generalSearch").click()
time.sleep(12)
driver.find_element_by_xpath("//div[@class='list-container']/ul/li[1]/div[1]//div[@class='item-footer']/div/a[1]").click()
#driver.find_element_by_partial_link_text("详览").click()

time.sleep(12)

driver.switch_to.window(driver.window_handles[1])
print(driver.page_source)

name = driver.window_handles
print(name)






import requests
import json
URL = "http://www.ccgp-guangxi.gov.cn/front/search/category"
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    "Cookie": "acw_tc=76b20fe616014335008784406e5781f62c8032c2c5aa073e29d0ea51e47833",

}
data = {"categoryCode":"ZcyAnnouncement1","pageSize":15,"pageNo":1}

r = requests.post(url=URL,headers=headers,data=json.dumps(data))
print(r.status_code)
print(r.text)
print(json.dumps(data))

import time
from urllib.request import urlretrieve
import requests
from selenium import webdriver
url = "https://www.tianyancha.com/"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(8)
driver.find_element_by_xpath("//a[text()='登录/注册']").click()
driver.find_element_by_xpath("//div[text()='密码登录']").click()
time.sleep(4)
driver.find_element_by_id("mobile").send_keys("18309297863")
time.sleep(3)
driver.find_element_by_id("password").send_keys("qinlongmei950202")
time.sleep(3)
driver.find_element_by_xpath("//div[text()='登录']").click()
time.sleep(4)
print(driver.page_source)
print(driver.window_handles)

import requests
#url = "http://218.60.146.4/pubsearch/patentsearch/showFullText-viewFullText.shtml"
url = "http://218.60.146.4/pubsearch/search-ui/app/searchtools/js/examine.js?_=1602034155967"
data = {
    "nrdAn": "CN201921803014",
    "cid": "CN201921803014.120200731XX",
    "sid": "CN201921803014.120200731XX",

}
headers = {
    "Cookie": "WEE_SID=E3C89C85915A1ACC9A1679319C28369B.pubsearch02; IS_LOGIN=true; JSESSIONID=E3C89C85915A1ACC9A1679319C28369B.pubsearch02; avoid_declare=declare_pass",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",

}
#r = requests.post(url,data=data,headers=headers)
r = requests.get(url,headers=headers)
print(r.status_code)
print(r.text)

import xmltodict
import json
import re
from lxml import etree
value = '''<?xml version="1.0" encoding="UTF-8"?><div xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:siposeas="java:com.neusoft.sipo.sipopublicsearch.search.app.view.detailUtils.xsltParser.XsltSeasParser" xmlns:str="http://example.com/namespace" xmlns:business="http://www.sipo.gov.cn/XMLSchema/business" xmlns:base="http://www.sipo.gov.cn/XMLSchema/base" xmlns:tbl="http://oasis-open.org/specs/soextblx" class="fullText"><table><tr><td id="claim_title" class="header">权利要求书</td></tr><tr><td class="content" id="claim_1"><business:ClaimText>1.一种陶瓷型芯成型机压注加料装置，其特征在于，包括储料罐，所述储料罐上设有搅拌轴，搅拌轴的搅拌部置于储料罐腔体内，搅拌轴的上端置于腔体外；所述储料罐下方设有抽浆口，抽浆口与料阀体连通，料阀体的一端设有封闭气缸；料阀体下端与抽料缸连接，抽料缸与滑阀体连接；抽料缸的一端设有输浆口，所述输浆口连接单向阀，所述单向阀与输浆管连接，所述输浆管与注浆杯连接；所述滑阀体的另一端连接滑阀连杆，该端滑阀体还通过气缸连杆和法兰与注料驱动气缸连接；所述输浆管外套有柔性加热套，所述储料罐外设有柔性加热器；所述滑阀体为伴热滑阀体。</business:ClaimText></td></tr><tr><td class="content" id="claim_2"><business:ClaimText>2.根据权利要求1所述的一种陶瓷型芯成型机压注加料装置，其特征在于，所述搅拌轴上端可外接搅拌电机。</business:ClaimText></td></tr><tr><td class="content" id="claim_3"><business:ClaimText>3.根据权利要求1所述的一种陶瓷型芯成型机压注加料装置，其特征在于，所述输浆管采用柔性管道或刚性管道。</business:ClaimText></td></tr><tr><td class="content" id="claim_4"><business:ClaimText>4.根据权利要求1所述的一种陶瓷型芯成型机压注加料装置，其特征在于，伴热抽送浆滑阀体具体为：滑阀体的双侧设有铸铝加热板，所述铸铝加热板上设有控温热电阻。</business:ClaimText></td></tr><tr><td class="content" id="claim_5"><business:ClaimText>5.根据权利要求1所述的一种陶瓷型芯成型机压注加料装置，其特征在于，该装置所有与浆料接触的位置都有柔性加热带。</business:ClaimText></td></tr></table></div><div xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:siposeas="java:com.neusoft.sipo.sipopublicsearch.search.app.view.detailUtils.xsltParser.XsltSeasParser" xmlns:str="http://example.com/namespace" xmlns:business="http://www.sipo.gov.cn/XMLSchema/business" xmlns:base="http://www.sipo.gov.cn/XMLSchema/base" xmlns:tbl="http://oasis-open.org/specs/soextblx" class="fullText"><table style="table-layout:fixed"><tr><td id="description_title" class="header">说明书</td></tr><tr><td class="content" id="description_invention_title">一种陶瓷型芯成型机压注加料装置</td></tr><tr><td class="content" id="description_1">技术领域</td></tr><tr><td class="content" id="description_2">本实用新型涉及陶瓷型芯成型技术领域，尤其是一种陶瓷型芯成型机压注加料装置。</td></tr><tr><td class="content" id="description_3">背景技术</td></tr><tr><td class="content" id="description_4">陶瓷型芯用于在熔模铸造中形成铸件的复杂精密空腔。当陶瓷型芯的成型设备采用顶注式的气动成型机时，往往采用勺子手动加料的方式。加料过程中浆料容易出现浆料散落、污染、效率低等缺点。</td></tr><tr><td class="content" id="description_5">实用新型内容</td></tr><tr><td class="content" id="description_6">本实用新型的技术任务是针对以上现有技术的不足，而提供一种陶瓷型芯成型机压注加料装置。</td></tr><tr><td class="content" id="description_7">本实用新型解决其技术问题所采用的技术方案是：一种陶瓷型芯成型机压注加料装置，包括储料罐，所述储料罐上设有搅拌轴，搅拌轴的搅拌部置于储料罐腔体内，搅拌轴的上端置于腔体外；所述储料罐下方设有抽浆口，抽浆口与料阀体连通，料阀体的一端设有封闭气缸；料阀体下端与抽料筒连接，抽料筒与滑阀体连接；抽料筒的一端设有输浆口，所述输浆口连接单向阀，所述单向阀与输浆管连接，所述输浆管与注浆杯连接；所述滑阀体的另一端连接滑阀连杆，该端滑阀体还通过气缸连杆和法兰与注料驱动气缸连接；所述输浆管外套有柔性加热套，所述储料罐外设有柔性加热器；所述滑阀体为伴热滑阀体。</td></tr><tr><td class="content" id="description_8">所述搅拌轴上端可外接搅拌电机。</td></tr><tr><td class="content" id="description_9">所述输浆管采用柔性管道或刚性管道。</td></tr><tr><td class="content" id="description_10">伴热抽送浆滑阀体具体为：滑阀体的双侧设有铸铝加热板，所述铸铝加热板上设有控温热电阻。</td></tr><tr><td class="content" id="description_11">该装置所有与浆料接触的位置都有柔性加热带。</td></tr><tr><td class="content" id="description_12">本实用新型的优点：</td></tr><tr><td class="content" id="description_13">本实用新型在陶瓷型芯的成型注料时具有加料速度快；加料过程完全封闭，无浆料散落、污染等优点。</td></tr><tr><td class="content" id="description_14">附图说明</td></tr><tr><td class="content" id="description_15">图1是本实用新型的整体结构示意图；</td></tr><tr><td class="content" id="description_16">图2是本实用新型的局部剖面图；</td></tr><tr><td class="content" id="description_17">图3是本实用新型的整体剖面图。</td></tr><tr><td class="content" id="description_18">具体实施方式</td></tr><tr><td class="content" id="description_19">下面结合说明书附图对本实用新型做以下详细说明。</td></tr><tr><td class="content" id="description_20">如图所示，一种陶瓷型芯成型机压注加料装置，包括储料罐1，所述储料罐上设有搅拌轴2，搅拌轴2的搅拌部21置于储料罐腔体内，搅拌轴的上端22置于腔体外；所述储料罐1下方设有抽浆口3，抽浆口3与料阀体4连通，料阀体4的一端设有封闭气缸5；料阀体4下端设有抽料缸12，抽料缸12与滑阀体连接，抽料缸12的一端设有输浆口7，所述输浆口7连接单向阀8，所述单向阀8与输浆管9连接，所述输浆管9与注浆杯10连接；所述滑阀体6的另一端连接滑阀连杆61，该端滑阀体6还通过气缸连杆62和法兰63与注料驱动气缸11连接；所述输浆管9外套有柔性加热套，所述储料罐1外设有柔性加热器；所述滑阀体6为伴热滑阀体。</td></tr><tr><td class="content" id="description_21">所述搅拌轴上端22可外接搅拌电机。</td></tr><tr><td class="content" id="description_22">所述输浆管9采用柔性管道或刚性管道。</td></tr><tr><td class="content" id="description_23">伴热抽送浆滑阀体具体为：滑阀体的双侧设有铸铝加热板，所述铸铝加热板上设有控温热电阻。</td></tr><tr><td class="content" id="description_24">该装置所有与浆料接触的位置都有柔性加热带。</td></tr><tr><td class="content" id="description_25">储料罐中的浆料由抽浆口流出到料阀体；封闭气缸，当从储料罐抽料时推动封闭气缸活塞，使储料罐与下方的抽料缸连通。当注料时，推动活塞关闭与储料罐的连接；注料气缸，注料时推动活塞将料射出。滑阀由注料驱动气缸驱动，控制气缸行程同时控制输浆容积。</td></tr><tr><td class="content" id="description_26">以上所述仅为本实用新型的实施例，并非因此限制本实用新型的专利范围，凡是利用本实用新型说明书及附图内容所作的等效结构或等效流程变换，或直接或间接运用在其他相关的技术领域，均同理包括在本实用新型的专利保护范围内。</td></tr></table></div>'''
#data = xmltodict.parse(value)
#data = re.findall("[\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a]",value)

#data = json.dumps(data,ensure_ascii=False)
#text = data['#text']
#data = data['RESULT']['table']['tr']['td']['business:Abstract']['base:Paragraphs']['#text']
#data = json.loads(data)
#text = data['RESULT']['table']['tr']['td']['business:Abstract']['base:Paragraphs']['#text']
#print(text)
html = etree.HTML(value.encode('utf-8'))
content = html.xpath("//div[1]/table/tr/td//text()")
data = html.xpath("//div[2]/table/tr/td//text()")
print(content)
print(11111)
print(data)


import pandas as pd
data = pd.read_csv('company_name.csv',header=None)
name = data[0]
name_list = []
for i in name:
    #print(i)
    name_list.append(i)
print(name_list)

import re

list = [{'domain': '218.60.146.4', 'httpOnly': False, 'name': 'JSESSIONID', 'path': '/pubsearch', 'secure': False, 'value': '6D27E6FA9D02D4848C46333E89DAEE5F.pubsearch06'}, {'domain': '218.60.146.4', 'httpOnly': False, 'name': 'IS_LOGIN', 'path': '/pubsearch/portal', 'secure': False, 'value': 'false'}, {'domain': '218.60.146.4', 'httpOnly': False, 'name': 'WEE_SID', 'path': '/pubsearch/portal', 'secure': False, 'value': '6D27E6FA9D02D4848C46333E89DAEE5F.pubsearch06'}]
cookies = []
for i in range(len(list)):
    print(i)
    name = list[i]['name']
    value = list[i]['value']
    if i == len(list)-1:
        cookie = name + "=" + value
    else:
        cookie = name + "=" + value + ';'
    cookies.append(cookie)
    cookies_value = ''.join(cookies)
    cookies_value = re.sub("false",'true',cookies_value)

print(cookies_value)

import pytesseract
import requests
headers = {

    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}


def parse_code():
    text = pytesseract.image_to_string("code.png")
    return text


def get_img(s):
    img_url = 'http://218.60.146.4/pubsearch/portal/login-showPic.shtml'
    r = s.get(url=img_url, headers=headers)
    with open('code.png', 'wb') as f:
        f.write(r.content)

def get_url_cookies(s,text):

    url = 'http://218.60.146.4/pubsearch/wee/platform/wee_security_check?v=20201016'

    headers = {
        "Origin": "http://218.60.146.4",
        "Host": "218.60.146.4",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "http://218.60.146.4/pubsearch/portal/uilogin-forwardLogin.shtml",
        "Upgrade-Insecure-Requests": "1",

        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    data = {
        "j_loginsuccess_url":"",
        "j_validation_code": text,
        "j_username": "bmxwZmZfMTIzNA==",
        "j_password": "bmxwMTJfMzQ=",
    }
    #data = "j_validation_code={}&j_username=REJLSkRTQzIwMjA%3D&j_password=REJLSkRTQzIwMjA%3D".format(code)
    r = s.post(url=url, headers=headers, data=data)
    cookies = requests.utils.dict_from_cookiejar(r.cookies)
    cookies = "IS_LOGIN=" + cookies['IS_LOGIN'] +";" + " " + "WEE_SID" + cookies['WEE_SID'] + ""
    print(cookies)








if __name__ == '__main__':
    # 创建会话
    s = requests.Session()
    # 获取照片
    get_img(s)
    # parse_code
    text = parse_code()
    # 登录获取cookies
    get_url_cookies(s,text)


import time
from PIL import Image
from selenium import webdriver


from PIL import Image
from selenium import webdriver
url = "http://218.60.146.4/pubsearch/portal/uilogin-forwardLogin.shtml"
driver = webdriver.Chrome()
driver.maximize_window()  # 将浏览器最大化
driver.get(url)
# 截取当前网页并放到D盘下命名为printscreen，该网页有我们需要的验证码
driver.save_screenshot('printscreen.png')
imgelement = driver.find_element_by_id('codePic')  # 定位验证码
location = imgelement.location  # 获取验证码x,y轴坐标
print(location)
size = imgelement.size  # 获取验证码的长宽
print(size)
rangle = (int(location['y'] + 305), int(location['y'] + 335), int(location['x'] + 1121),
          int(location['x'] + size['height'] + 1121))  # 写成我们需要截取的位置坐标
i = Image.open("printscreen.png")  # 打开截图
frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
frame4 = frame4.convert('RGB')
frame4.save('save.jpg')  # 保存我们接下来的验证码图片 进行打码

driver.close()

# coding:utf-8
import sys, os

import pytesseract
from PIL import Image, ImageDraw


# 二值判断,如果确认是噪声,用改点的上面一个点的灰度进行替换
# 该函数也可以改成RGB判断的,具体看需求如何
def getPixel(image, x, y, G, N):
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
def clearNoise(image, G, N, Z):
    draw = ImageDraw.Draw(image)

    for i in range(0, Z):
        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                color = getPixel(image, x, y, G, N)
                if color != None:
                    draw.point((x, y), color)


# 测试代码
def main():
    # 打开图片
    image = Image.open("real_code.png")

    # 将图片转换成灰度图片
    image = image.convert("L")

    # 去噪,G = 50,N = 4,Z = 4
    clearNoise(image, 50, 4, 4)

    # 保存图片
    image.save("new_code.png")

def run():
    text = pytesseract.image_to_string("real_code.png")
    print(text)

if __name__ == '__main__':
    run()

"""



