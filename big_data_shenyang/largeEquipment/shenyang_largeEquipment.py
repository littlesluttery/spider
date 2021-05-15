#-*- coding=utf-8 -*-
#@Time : 2020/9/28 11:12 AM
#@Author : 小邋遢
#@File : shenyang_largeEquipment.py
#@Software : PyCharm
'''
目标网站：沈阳市科技条件平台
URL= "http://www.sykjtjpt.cn/h/equip/largeEquipment"
'''
import re

import pymysql
import requests
from pyquery import PyQuery as pq
from lxml import etree
from multiprocessing import Pool
from largeEquipment.config import *
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}

# 获取总的页数
def total_page_numbers():
    url = "http://www.sykjtjpt.cn/h/equip/largeEquipment"
    r = requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            doc = pq(r.text)
            total_page_number = doc('#page > div > ul > li:nth-child(11) > a').text()
            return total_page_number
        else:
            return None
    except ConnectionError:
        print("Error of parsing the total number of pages")

# 获取每一页的url
def parse_page(request_url):
    r = requests.get(url=request_url,headers=headers)
    try:
        if r.status_code == 200:
            html = etree.HTML(r.text)
            page_url = html.xpath("//div[@class='product-info']/h4/a/@href")
            return page_url
        else:
            return None
    except ConnectionError:
        print("Error of parsing each page URL")

def coonect_mysql():
    db = pymysql.connect(**CONFIG)
    cursor = db.cursor()
    return db,cursor

def id_is(key_id):
    db, cursor = coonect_mysql()
    # 判断数据是否存在
    sql = 'select key_id from equipment where key_id="{}"'.format(key_id)
    data = pd.read_sql_query(sql, db)
    # print(data)
    # if data['name']:
    # for item in data["key_id"]:
    if len(data["key_id"]) != 0:
        print("该设备已经存在数据库....")
        return 1
    else:
        return 0



def save_to_mysql(results):
    print("正在保存数据......")
    db, cursor = coonect_mysql()
    key_id = results["key_id"]
    key_id = ''.join(key_id)
    equipment_name = results["equipment_name"]
    specification_model = results["specification_model"]
    instrument_classification = results["instrument_classification"]
    workCompany = results["workCompany"]
    manufacturer = results["manufacturer"]
    production_country = results["production_country"]
    status_of_use = results["status_of_use"]
    technical_index = results["technical_index"]
    asset_code = results["asset_code"]
    classification_code = results["classification_code"]
    purchase_code = results["purchase_code"]
    main_accessories = results["main_accessories"]
    technical_characteristics = results["technical_characteristics"]
    number_of_services = results["number_of_services"]
    praise_rate = results["praise_rate"]
    volume = results["volume"]
    main_function = results['main_function']

    sql = 'insert into equipment(equipment_name,specification_model,  instrument_classification,workCompany,manufacturer,production_country,status_of_use,technical_index,asset_code,classification_code,purchase_code,main_accessories,technical_characteristics,number_of_services,praise_rate,volume,main_function,key_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(sql, (equipment_name,specification_model,  instrument_classification,workCompany,manufacturer,production_country,status_of_use,technical_index,asset_code,classification_code,purchase_code,main_accessories,technical_characteristics,number_of_services,praise_rate,volume,main_function,key_id))

        db.commit()
        print("保存到数据库成功！")
        cursor.close()
        db.close()
    except Exception:
        print("save_data_mysql is failed！")


# 获取每一个url的详情信息
def parse_page_detail(url,key_id):
    print("正在抓取设备......")
    flag = id_is(key_id)
    if flag == 0:
        r = requests.get(url, headers=headers)
        try:
            if r.status_code == 200:

                html = etree.HTML(r.text)
                # manufacturer:生产厂商/制造厂商
                manufacturer = html.xpath("//div[@class='present-right']/div/span[1]//text()")
                manufacturer = ''.join(manufacturer).strip()
                manufacturer = manufacturer.split("：")[1].strip()
                # equipment_name:仪器名称
                equipment_name = html.xpath("//p[@class='equipTitle']/text()")
                equipment_name = ''.join(equipment_name).strip()
                # asset_code:资产编码
                asset_code = html.xpath("//div[@class='present-right']/div/span[2]//text()")
                asset_code = ''.join(asset_code).strip()
                asset_code = asset_code.split("：")[1].strip()
                # production_country:生产国别
                production_country = html.xpath("//div[@class='present-right']/div/span[3]//text()")
                production_country = ''.join(production_country)
                production_country = production_country.split("：")[1].strip()
                # instrument_classification:仪器分类
                instrument_classification = html.xpath("//div[@class='present-right']/div/span[4]//text()")
                instrument_classification = ''.join(instrument_classification)
                instrument_classification = instrument_classification.split("：")[1].strip()
                # classification_code:分类编码
                classification_code = html.xpath(
                    "//div[@class='details col-lg-9 col-md-9 col-sm-9']/table[1]/tbody/tr[1]/td[1]/text()")
                classification_code = ''.join(classification_code).strip()
                # purchase_code:购置日期
                purchase_code = html.xpath(
                    "//div[@class='details col-lg-9 col-md-9 col-sm-9']/table[1]/tbody/tr[2]/td[1]/text()")
                purchase_code = ''.join(purchase_code).strip()
                # specification_model:规格型号
                specification_model = html.xpath(
                    "//div[@class='details col-lg-9 col-md-9 col-sm-9']/table[1]/tbody/tr[3]/td[1]/text()")
                specification_model = ''.join(specification_model).strip()
                # instrument_status:仪器状态
                status_of_use = html.xpath(
                    "//div[@class='details col-lg-9 col-md-9 col-sm-9']/table[1]/tbody/tr[4]/td[1]/text()")
                status_of_use = ''.join(status_of_use).strip()
                # features:功能
                main_function = html.xpath(
                    "//div[@class='details col-lg-9 col-md-9 col-sm-9']/table[2]/tbody/tr[1]/td[1]/text()")
                main_function = ''.join(main_function).strip()
                # main_accessories:主要附件
                main_accessories = html.xpath(
                    "//div[@class='details col-lg-9 col-md-9 col-sm-9']/table[2]/tbody/tr[2]/td[1]/text()")
                main_accessories = ''.join(main_accessories).strip()
                # technical_index :技术指标
                technical_index = html.xpath(
                    "//div[@class='details col-lg-9 col-md-9 col-sm-9']/table[2]/tbody/tr[3]/td[1]/text()")
                technical_index = ''.join(technical_index).strip()
                # technical_characteristics:技术特色
                technical_characteristics = html.xpath(
                    "//div[@class='details col-lg-9 col-md-9 col-sm-9']/table[2]/tbody/tr[4]/td[1]/text()")
                technical_characteristics = ''.join(technical_characteristics).strip()
                # workCompany:所属单位
                workCompany = html.xpath("//div[@class='shop']/p[2]/text()")
                workCompany = ''.join(workCompany).strip()
                # number_of_services:服务数
                number_of_services = html.xpath("//table[@class='shop-data']/tbody/tr/th[1]/text()")
                number_of_services = ''.join(number_of_services).strip()
                # praise_rate:好评率
                praise_rate = html.xpath("//table[@class='shop-data']/tbody/tr/th[2]/text()")
                praise_rate = ''.join(praise_rate).strip()
                # volume:成交量
                volume = html.xpath("//table[@class='shop-data']/tbody/tr/th[3]/text()")
                volume = ''.join(volume).strip()
                key_id = key_id
                results = {
                    "manufacturer": manufacturer,
                    "equipment_name": equipment_name,
                    "asset_code": asset_code,
                    "production_country": production_country,
                    "instrument_classification": instrument_classification,
                    "classification_code": classification_code,
                    "purchase_code": purchase_code,
                    "specification_model": specification_model,
                    "status_of_use": status_of_use,
                    "main_function": main_function,
                    "main_accessories": main_accessories,
                    "technical_index": technical_index,
                    "technical_characteristics": technical_characteristics,
                    "workCompany": workCompany,
                    "number_of_services": number_of_services,
                    "praise_rate": praise_rate,
                    "volume": volume,
                    "key_id": key_id,
                }
                if results:
                    save_to_mysql(results)
                # print(results)


        except ConnectionError:
            print("Error of parsing details page")


def main(groups):

        # 构造重定向url
        request_url = "http://www.sykjtjpt.cn/h/equip/equipmentList?searchText=&tabId=allEquipment&sortId=&codeField=&allEquipPageNum=0&allEquipNumPerPage=0&allEquipTotalCount=0&pageNo={}&pageSize=0".format(groups)
        # 拿到索引页
        page_urls = parse_page(request_url)
        for url in page_urls:
            url = "http://www.sykjtjpt.cn" + url
            key_id = re.findall("orinId=(.*)", url)
            key_id = ''.join(key_id)
            # 解析详情页数据
            parse_page_detail(url,key_id)
            
if __name__ == '__main__':

    # 使用原始url，得到总页码数
    total_page_number = total_page_numbers()
    groups = [x for x in range(1,int(total_page_number)+1)]
    pool =  Pool()
    pool.map(main,groups)
    pool.close()
    pool.join()
    
    
    