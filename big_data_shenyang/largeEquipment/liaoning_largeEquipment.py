#-*- coding=utf-8 -*-
#@Time : 2020/9/28 11:12 AM
#@Author : 小邋遢
#@File : liaoning_largeEquipment.py
#@Software : PyCharm
'''
目标网站：辽宁省大型科学仪器共享服务平台
url："http://www.liaoninglab.com/index/dxyqfront/instrument/list"
'''
import re

import pymysql
import requests
from pyquery import PyQuery as pq
from lxml import etree
from multiprocessing import Pool
import pandas as pd

from largeEquipment.config import *

url = "http://www.liaoninglab.com/index/dxyqfront/instrument/list"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"

}

def total_page_numbers():
    r = requests.get(url,headers=HEADERS)
    try:
        if r.status_code == 200:
            doc = pq(r.text)
            total_page_number = doc('body > div.container.warp > div > div.c-content > div.page.clearfix > div > ul > li:nth-child(11) > a').text()
            return total_page_number
        return None
    except ConnectionError:
        print("Error of parsing the total number of pages")


def page_urls(i):
    data = {
        "pageNo": i,
        "pageSize": 15,
        "yqtype": "",
        "area": "",
        "name": "",
    }
    r = requests.post(url,headers=HEADERS,data=data)
    try:
        if r.status_code == 200:
            html = etree.HTML(r.text)
            urls = html.xpath("//div[@class='listbox']/ul/li/a/@href")
            return urls
        else:
            return None
    except ConnectionError:
        print("Error of parsing each page URL")


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


def parse_page_detail(url,key_id):
    print("正在抓取设备数据......")
    flag = id_is(key_id)
    if flag == 0:
        r = requests.get(url, headers=HEADERS)
        try:
            if r.status_code == 200:
                print(url)
                print(r.status_code)
                # print(r.text)
                html = etree.HTML(r.text)
                # equipment_name:仪器名称
                equipment_name = html.xpath("//div[@class='c-for']/h2/text()")
                equipment_name = ''.join(equipment_name).strip()
                # specification_model:规格型号
                specification_model = html.xpath("//div[@class='c-for']/ul/li[1]/text()")
                specification_model = ''.join(specification_model).strip()
                # instrument_classification:仪器分类
                instrument_classification = html.xpath("//div[@class='c-for']/ul/li[2]/text()")
                instrument_classification = ''.join(instrument_classification).strip()
                # original_instrument_value:仪器原值
                original_instrument_value = html.xpath("//div[@class='c-for']/ul/li[3]/text()")
                original_instrument_value = ''.join(original_instrument_value).strip()
                # workCompany:所属单位
                workCompany = html.xpath("//div[@class='c-for']/ul/li[4]/text()")
                workCompany = ''.join(workCompany)
                # manufacturer:生产厂商/制造厂商
                manufacturer = html.xpath("//div[@class='c-for']/ul/li[5]/text()")
                manufacturer = ''.join(manufacturer).strip()
                # production_country:生产国别 /产地国别
                production_country = html.xpath("/div[@class='c-for']/ul/li[6]/text()")
                production_country = ''.join(production_country)
                # supplier:供货商
                supplier = html.xpath("//div[@class='c-for']/ul/li[7]/text()")
                supplier = ''.join(supplier).strip()
                # located_area_instrument:仪器所在地区
                located_area_instrument = html.xpath("//div[@class='c-for']/ul/li[8]/text()")
                located_area_instrument = ''.join(located_area_instrument).strip()
                # instrument_placement_address:仪器安放地址
                instrument_placement_address = html.xpath("//div[@class='c-for']/ul/li[9]/text()")
                instrument_placement_address = ''.join(instrument_placement_address).strip()
                # contact_person:联 系 人
                contact_person = html.xpath("//div[@class='conbox'][1]//div[@class='companyinf jbxx']/ul/li[1]/text()")
                contact_person = ''.join(contact_person).strip()
                # contact_number:联系电话
                contact_number = html.xpath("//div[@class='conbox'][1]//div[@class='companyinf jbxx']/ul/li[2]/text()")
                contact_number = ''.join(contact_number).strip()
                # charges:收费标准
                charges = html.xpath("//div[@class='conbox'][1]//div[@class='companyinf jbxx']/ul/li[3]/text()")
                charges = ''.join(charges).strip()
                # hourly_occupancy_fee:每小时占用费
                hourly_occupancy_fee = html.xpath(
                    "//div[@class='conbox'][1]//div[@class='companyinf jbxx']/ul/li[4]/text()")
                hourly_occupancy_fee = ''.join(hourly_occupancy_fee).strip()
                # email:电子邮箱
                email = html.xpath("//div[@class='conbox'][1]//div[@class='companyinf jbxx']/ul/li[5]/text()")
                email = ''.join(email).strip()
                # device_id:设备编号
                device_id = html.xpath("//div[@class='conbox'][2]//div[@class='companyinf jbxx']/ul/li[1]/text()")
                device_id = ''.join(device_id).strip()
                # effective_time_per_year:年有效机时
                effective_time_per_year = html.xpath(
                    "//div[@class='conbox'][2]//div[@class='companyinf jbxx']/ul/li[2]/text()")
                effective_time_per_year = ''.join(effective_time_per_year).strip()
                # external_sharing_machine_time:对外共享机时
                external_sharing_machine_time = html.xpath(
                    "/div[@class='conbox'][2]//div[@class='companyinf jbxx']/ul/li[3]/text()")
                external_sharing_machine_time = ''.join(external_sharing_machine_time).strip()
                # status_of_use:使用状态
                status_of_use = html.xpath("//div[@class='conbox'][2]//div[@class='companyinf jbxx']/ul/li[4]/text()")
                status_of_use = ''.join(status_of_use).strip()
                # operating_status:运行状态
                operating_status = html.xpath(
                    "//div[@class='conbox'][2]//div[@class='companyinf jbxx']/ul/li[5]/text()")
                operating_status = ''.join(operating_status).strip()
                # technical_index :技术指标
                technical_index = html.xpath("//div[@class='conbox'][3]//div[@class='companyinf jbwz']//text()")
                technical_index = ''.join(technical_index).strip()
                # features:功能
                features = html.xpath("//div[@class='conbox'][4]//div[@class='companyinf jbwz']//text()")
                features = ''.join(features).strip()
                # instrument_introduction:仪器简介
                instrument_introduction = html.xpath("//div[@class='conbox'][5]//div[@class='companyinf jbwz']//text()")
                instrument_introduction = ''.join(instrument_introduction).strip()
                # main_accessories:主要附件
                main_accessories = html.xpath("//div[@class='conbox'][6]//div[@class='companyinf jbwz']//text()")
                main_accessories = ''.join(main_accessories).strip()
                results = {
                    "equipment_name": equipment_name,
                    "specification_model": specification_model,
                    "instrument_classification": instrument_classification,
                    "original_instrument_value": original_instrument_value,
                    "workCompany": workCompany,
                    "manufacturer": manufacturer,
                    "production_country": production_country,
                    'supplier': supplier,
                    "located_area_instrument": located_area_instrument,
                    "instrument_placement_address": instrument_placement_address,
                    "contact_person": contact_person,
                    "contact_number": contact_number,
                    "charges": charges,
                    "hourly_occupancy_fee": hourly_occupancy_fee,
                    "email": email,
                    "device_id": device_id,
                    "effective_time_per_year": effective_time_per_year,
                    "external_sharing_machine_time": external_sharing_machine_time,
                    "status_of_use": status_of_use,
                    'operating_status': operating_status,
                    "technical_index": technical_index,
                    "features": features,
                    "instrument_introduction": instrument_introduction,
                    "main_accessories": main_accessories,
                    "key_id": key_id,

                }
                print(results)
                return results
            else:
                return None
        except ConnectionError:
            print("error")
            parse_page_detail(url)


def coonect_mysql():
    db = pymysql.connect(**CONFIG)
    cursor = db.cursor()
    return db,cursor


def save_to_mysql(results):
    db,cursor = coonect_mysql()
    equipment_name = results["equipment_name"]
    specification_model = results["specification_model"]
    instrument_classification = results["instrument_classification"]
    original_instrument_value = results["original_instrument_value"]
    workCompany = results["workCompany"]
    manufacturer = results["manufacturer"]
    production_country = results["production_country"]
    supplier = results["supplier"]
    located_area_instrument = results["located_area_instrument"]
    instrument_placement_address = results["instrument_placement_address"]
    contact_person = results["contact_person"]
    contact_number = results["contact_number"]
    charges = results["charges"]
    hourly_occupancy_fee = results["hourly_occupancy_fee"]
    email = results["email"]
    device_id = results["device_id"]
    effective_time_per_year = results["effective_time_per_year"]
    external_sharing_machine_time = results["external_sharing_machine_time"]
    status_of_use = results["status_of_use"]
    operating_status = results["operating_status"]
    technical_index = results["technical_index"]
    main_function = results["features"]
    instrument_introduction = results["instrument_introduction"]
    main_accessories = results["main_accessories"]
    key_id = results["key_id"]
    key_id = ''.join(key_id)
    sql = 'insert into equipment(equipment_name,specification_model,instrument_classification,original_instrument_value,workCompany, manufacturer,production_country,supplier,located_area_instrument,instrument_placement_address,contact_person,contact_number,charges,hourly_occupancy_fee,email,device_id,effective_time_per_year,external_sharing_machine_time,status_of_use,operating_status,technical_index,main_function,instrument_introduction,main_accessories,key_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    #sql = 'insert into equipment(equipment_name)'
    try:
        cursor.execute(sql,(equipment_name,specification_model,instrument_classification,original_instrument_value,workCompany, manufacturer,production_country,supplier,located_area_instrument,instrument_placement_address,contact_person,contact_number,charges,hourly_occupancy_fee,email,device_id,effective_time_per_year,external_sharing_machine_time,status_of_use,operating_status,technical_index,main_function,instrument_introduction,main_accessories,key_id))

        db.commit()
        print("保存到数据库成功！")
        cursor.close()
        db.close()
    except Exception:
        print("save_data_mysql is failed！")
        db.rollback()
        save_to_mysql(results)


def main(i):
        # 获取列表页每一个url
        urls = page_urls(i)
        for url in urls:
            url = "http://www.liaoninglab.com" + url
            #print(url)
            key_id = re.findall("id=(.*)",url)
            key_id = ''.join(key_id)
            #print(key_id)
            # 获取详情页数据
            results = parse_page_detail(url,key_id)
            # 保存数据到数据库
            if results:
                save_to_mysql(results)






if __name__ == '__main__':

    # 拿到总的页码数
    total_page_number = total_page_numbers()
    groups = [i for i in range(1,int(total_page_number)+1)]
    pool = Pool()
    pool.map(main,groups)
    pool.close()
    pool.join()