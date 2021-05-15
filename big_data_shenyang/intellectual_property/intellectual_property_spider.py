#-*- coding=utf-8 -*-
#@Time : 2020/10/1 9:44 AM
#@Author : 小邋遢
#@File : intellectual_property_spider.py
#@Software : PyCharm
import cv2

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from intellectual_property.config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import etree
from selenium.webdriver.chrome.options import Options
from urllib.request import urlretrieve
from PIL import Image
from pytesseract import pytesseract

from selenium.webdriver.chrome.options import Options

from big_data_shenyang.intellectual_property.config import START_URL

chrome_options = Options()
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('disable-dev-shm-usage')
chrome_options.add_argument('--headless')
#driver = webdriver.PhantomJS()
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 100)


def search_company_name(name):
    print("正在专利检索页面进行搜索.......")
    try:
        driver.get(url=SEARCH_URL)
        input = wait.until(EC.presence_of_element_located((By.ID,'search_input')))
        input.send_keys(name)
        search = wait.until(EC.element_to_be_clickable((By.ID,'btn_generalSearch')))
        search.click()

    except TimeoutException:
        #search_company_name(name)
        print("搜索出错.......")


def parse_code():
    driver.save_screenshot('code.png')
    img = cv2.imread('code.png')
    cro = img[1042:1106,2282:2397]
    cv2.imwrite('real_code.png', cro)
    text = pytesseract.image_to_string("real_code.png")
    return text




def login():
    print("正在登录专利检索系统.......")
    try:
        driver.get(url=START_URL)
        username = wait.until(EC.presence_of_element_located((By.ID, 'j_username')))
        password = wait.until(EC.presence_of_element_located((By.ID, 'j_password_show')))
        code = wait.until(EC.presence_of_element_located((By.ID, 'j_validation_code')))
        time.sleep(2)
        username.send_keys("DBKJDSC2020")
        time.sleep(2)
        password.send_keys("DBKJDSC2020")
        time.sleep(3)
        text = parse_code()
        time.sleep(10)
        code.send_keys(text)
        login = wait.until(EC.element_to_be_clickable((By.ID, 'login_btn_1 h-btn-blue1')))
        login.click()
    except Exception:
        print("登录出错")





def parse_details_data(agent,agency):
    html = etree.HTML(driver.page_source)
    # patent_name :专利名称
    patent_name = html.xpath("//span[@class='table-container-title']/text()")
    patent_name = ''.join(patent_name).strip()
    # application_number:申请号
    application_number = html.xpath("//tr[@class='tr_0']/td[2]/div//text()")
    application_number = ''.join(application_number).strip()
    # application_date:申请日
    application_date = html.xpath("//tr[@class='tr_0']/td[4]/div//text()")
    application_date = ''.join(application_date).strip()

    # public_number:公开号
    public_number = html.xpath("//tr[@class='tr_1']/td[2]/div//text()")
    public_number = ''.join(public_number).strip()
    # public_date:公开日
    public_date = html.xpath("//tr[@class='tr_1']/td[4]/div//text()")
    public_date = ''.join(public_date).strip()
    # priority_number:优先权号
    priority_number = html.xpath("//tr[@class='tr_2']/td[2]/div//text()")
    priority_number = ''.join(priority_number).strip()
    # priority_date:优先权日
    priority_date = html.xpath("//tr[@class='tr_2']/td[4]/div//text()")
    priority_date = ''.join(priority_date).strip()

    # IPC_classification_number:IPC分类号
    IPC_classification_number = html.xpath("//table[@class='custom']/tbody/tr[4]/td[2]/div/text()")
    IPC_classification_number = ''.join(IPC_classification_number).strip()

    # applicant:申请（专利权）人
    applicant = html.xpath("//table[@class='custom']/tbody/tr[5]/td[2]/div/text()")
    applicant = ''.join(applicant).strip()

    # inventor:发明人
    inventor = html.xpath("//table[@class='custom']/tbody/tr[6]/td[2]/div/text()")
    inventor = ''.join(inventor).strip()
    # applicant_address:申请人地址
    applicant_address = html.xpath("//table[@class='custom']/tbody/tr[7]/td[2]/div/text()")
    applicant_address = ''.join(applicant_address).strip()
    # applicant_zip_code:申请人邮编
    applicant_zip_code = html.xpath("//table[@class='custom']/tbody/tr[8]/td[2]/div/text()")
    applicant_zip_code = ''.join(applicant_zip_code).strip()

    # applicant_country:申请人所在国（省）
    applicant_country = html.xpath("//table[@class='custom']/tbody/tr[9]/td[2]/div/text()")
    applicant_country = ''.join(applicant_country).strip()

    # summary:摘要
    summary = html.xpath("//td[@class='content']//text()")
    summary = ''.join(summary).strip()

    results = {
        "patent_name": patent_name,
        "application_number": application_number,
        "application_date": application_date,
        "public_number": public_number,
        "public_date": public_date,
        "priority_number": priority_number,
        "priority_date": priority_date,
        "IPC_classification_number": IPC_classification_number,
        "applicant": applicant,
        "inventor": inventor,
        "applicant_address": applicant_address,
        "applicant_zip_code": applicant_zip_code,
        "applicant_country": applicant_country,
        "summary": summary,
        'agent': agent,
        "agency": agency,

    }
    print(results)



def parse_details():
    print("正在进入专利详情页.......")
    time.sleep(10)
    try:
        o_html = etree.HTML(driver.page_source)
        #print(driver.page_source)
        while True:
        #if o_html.xpath("//a[text()='下一页']"):

            number = o_html.xpath("//div[@class='list-container']/ul/li/div/div/h1/text()")

            for i in range(1,len(number)+1):
                print(i)
                try:
                    # agent:代理人
                    agent = o_html.xpath("//b[text()='代理人 : ']/../following-sibling::td/text()")[i]
                    agent = ''.join(agent).strip()
                except:
                    agent = ''
                try:
                    # agency:代理机构
                    agency = o_html.xpath("//b[text()='代理机构 : ']/../following-sibling::td/text()")[i]
                    agency = ''.join(agency)
                except:
                    agency = ''
                time.sleep(10)
                detail = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='list-container']/ul/li[{}]/div/div[3]/div/a[1]".format(i))))
                time.sleep(2)
                detail.click()
                try:
                    driver.switch_to.window(driver.window_handles[1])
                except:
                    print("error of driver handles")
                time.sleep(10)

                print("加载详情页完毕......")
                print(7)
                parse_details_data(agent,agency)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(4)


            time.sleep(2)
            next_page = wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='page_bottom']//a[text()='下一页']")))
            if next_page:
                next_page.click()
                time.sleep(7)
                #print(driver.page_source)
            else:
                break


    except TimeoutException:
        print("error")





def run():


        # 登录专利检索系统
        login()

        # 遍历从config读取企业列表，逐个进行抓取
        for name in COMPANY_NAME:
            # 进入搜索页进行名称搜索
            search_company_name(name)
            # 获取总页数

            # 在索引页进入每一个专利，获取详细信息。
            parse_details()





if __name__ == '__main__':
    run()