#-*- coding=utf-8 -*-
#@Time : 2020/10/9 12:52 PM
#@Author : 小邋遢
#@File : shenyang_expert_spider.py
#@Software : PyCharm
import json
import os
import re
from urllib.request import urlretrieve

import pymysql
import requests
from expert.config import *
from lxml import etree
import pandas as pd

def total_page_numbers():
    url = 'http://www.sykjtjpt.cn/h/talent/talentService'
    r = requests.get(url,headers=HEADERS)
    if r.status_code == 200:
        html = etree.HTML(r.text)
        total_page_number = html.xpath("//div[@id='pagination']/li/a/text()")[-2]
        total_page_number = ''.join(total_page_number)
        return total_page_number
    else:
        return None
def coonect_mysql():

    db = pymysql.connect(**CONFIG)
    cursor = db.cursor()
    return db,cursor

def id_is(key_id):
    db,cursor = coonect_mysql()
    # 判断数据是否存在
    sql = 'select key_id from expert where key_id="{}"'.format(key_id)
    data = pd.read_sql_query(sql, db)
    if len(data["key_id"]) != 0:
        print("该专家已经存在数据库....")
        return 1
    else:
        return 0

def save_to_msyql(results):
    db, cursor = coonect_mysql()
    key_id = results['key_id']
    #print(key_id)
    flag = id_is(key_id)
    if flag == 0:
        inventor = results['inventor']
        gender = results['gender']
        degrees = results['degrees']
        data_of_birth = results['data_of_birth']
        expert_title = results['expert_title']
        professional_field = results['professional_field']
        workCompany = results['workCompany']
        areas_of_expertise = results['areas_of_expertise']
        talent_profile = results['talent_profile']
        photo = results['photo']
        try:
            sql = 'insert into expert(inventor,key_id,gender,degrees,data_of_birth,expert_title,professional_field,workCompany,areas_of_expertise,talent_profile,photo) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (inventor,key_id,gender,degrees,data_of_birth,expert_title,professional_field,workCompany,areas_of_expertise,talent_profile,photo))
            db.commit()
            print("保存到数据库成功")
            cursor.close()
            db.close()
        except:
            save_to_msyql(results)
            print("保存到数据库失败......")


def save_img(photo_url,id):
    print("保存专家照片到本地.....")
    # 获取当前目录
    path = os.getcwd()
    file_path = path + "/expert_photo/" + "{}.png".format(id)
    try:
        urlretrieve(photo_url, file_path)
    except Exception:
        print("error of save expert photo")




def parse_page_url(i):
   data = {
        "pageNo": i,
        "pageSize": 12,
        "industrialField":"",
        "rank": "",
   }
   r = requests.post(url=DONGBEI_EXPERT_URL,headers=HEADERS,data=data)
   print(r.status_code)
   #print(r.text)
   if r.status_code == 200:
       data = json.loads(r.text)
       data = data['page']
       data = data['list']
       for i in range(12):
           data_1 = data[i]
           #print(data_1)
           key_id = data_1['expertId']
           # inventor：姓名
           inventor = data_1['name']
           # gender:性别
           gender = data_1['gender']
           #degree:学历
           degrees = data_1['degrees']
           try:
               # data_of_birth :出生年月
               data_of_birth = data_1['birthday']
           except:
               data_of_birth = None
           # expert_title:专家职称
           expert_title = data_1['rank']
           #professional_field:专业领域
           professional_field = data_1['industrialField']
           #workCompany:工作单位
           workCompany = data_1['unit']
           #areas_of_expertise:擅长领域
           areas_of_expertise = data_1['goodField']
           # talent_profile:人才简介
           talent_profile = data_1['intro']
           #photo:照片
           photo = data_1['imgPath']
           save_img(photo,key_id)
           results = {
               "inventor":inventor,
               "key_id":key_id,
               "gender":gender,
               "degrees":degrees,
               "data_of_birth":data_of_birth,
               "expert_title":expert_title,
               "professional_field":professional_field,
               "workCompany":workCompany,
               "areas_of_expertise":areas_of_expertise,
               "talent_profile":talent_profile,
               "photo":photo,
           }

           save_to_msyql(results)

   else:
       print(111)
       return None




def run():
    # 获取总页数
    total_page_number = total_page_numbers()
    print(total_page_number)
    for i in range(1,int(total_page_number)):
          parse_page_url(i)



if __name__ == '__main__':
    run()