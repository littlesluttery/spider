#-*- coding=utf-8 -*-
#@Time : 2020/9/30 5:59 PM
#@Author : 小邋遢
#@File : dongbei_expert_spider.py
#@Software : PyCharm
import json
import os
from urllib.request import urlretrieve
import requests
import re
from expert.config import *
import pymysql
import pandas as pd
import time

def parse_expert_id(url):

    r = requests.get(url,headers=HEADERS)
    try:
        if r.status_code == 200:
            #print(r.text)
            ids = re.findall('"id":(\d+)',r.text)
            #print(ids)
            return ids
        else:
            return None
    except Exception:
        print("error")


def save_img(photo_url,id):
    print("保存专家照片到本地.....")
    # 获取当前目录
    path = os.getcwd()
    file_path = path + "/expert_photo/" + "{}.png".format(id)
    try:
        urlretrieve(photo_url, file_path)
    except Exception:
        print("error of save expert photo")


def parse_expert_details(id):

    flag = id_is(id)
    print(flag)
    if flag == 0:
        data = {
            "id": id
        }
        #time.sleep(5)

        r = requests.post(url=EXPERT_ID, data=data)
        try:
            if r.status_code == 200:
                data = json.loads(r.text)

                data = data["data"]
                # name:姓名
                inventor = data["inventor"]
                # id：每个专家的固有id
                key_id = data["id"]
                # gender:性别
                gender = data["sex"]
                # expert_title:专家职称
                expert_title = data["titleName"]
                # data_of_birth:出生年月
                data_of_birth = data["birthday"]
                # workCompany:工作单位
                workCompany = data["workCompany"]
                # professional_field:从事专业/专业领域
                professional_field = data["nowWork"]
                # work_study_experience :学习或者工作经历
                work_study_experience = data["studyWorkHistory"]
                # research_direction:研究方向
                research_direction = data["searchDirect"]
                # research_results:研究成果
                research_results = data["searchResult"]
                # awards:获奖情况
                awards = data["honorInfo"]
                # photo:照片
                photo = data["profileUrl"]
                # 保存照片到本地
                save_img(photo, key_id)

                results = {
                    "inventor": inventor,
                    "key_id": key_id,
                    "gender": gender,
                    "expert_title": expert_title,
                    "data_of_birth": data_of_birth,
                    "workCompany": workCompany,
                    "professional_field": professional_field,
                    "work_study_experience": work_study_experience,
                    "research_direction": research_direction,
                    "research_results": research_results,
                    "awards": awards,
                    "photo": photo,

                }
                print(results)
                return results
            else:
                return None

        except Exception:
            print("error")
    else:
        pass

def coonect_mysql():

    db = pymysql.connect(**CONFIG)
    cursor = db.cursor()
    return db,cursor


def id_is(key_id):
    db,cursor = coonect_mysql()
    # 判断数据是否存在
    sql = 'select key_id from expert where key_id="{}"'.format(key_id)
    data = pd.read_sql_query(sql, db)
    # print(data)
    # if data['name']:
    #for item in data["key_id"]:
    if len(data["key_id"]) != 0:
        print("该专家已经存在数据库....")
        return 1
    else:
        return 0




def save_data_mysql(results):

        db, cursor = coonect_mysql()
        inventor = results["inventor"]
        gender = results["gender"]

        key_id = results["key_id"]

        data_of_birth = results["data_of_birth"]
        expert_title = results["expert_title"]
        workCompany = results["workCompany"]
        professional_field = results["professional_field"]
        work_study_experience = results["work_study_experience"]
        research_direction = results["research_direction"]
        research_results = results["research_results"]
        awards = results["awards"]
        photo = results["photo"]



        #sql = 'insert into expert(inventor,key_id,gender,data_of_birth,expert_title,workCompany,professional_field,work_study_experience,research_direction,research_results,awards,photo) values({},{},{},{},{},{},{},{},{},{},{},{})'.format(name,key_id, gender, data_of_birth, expert_title, workCompany, professional_field, work_study_experience,research_direction, research_results, awards, photo)
        sql = 'insert into expert(inventor,key_id,gender,data_of_birth,expert_title,workCompany,professional_field,work_study_experience,research_direction,research_results,awards,photo) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql,(inventor,key_id, gender, data_of_birth, expert_title, workCompany, professional_field, work_study_experience,research_direction, research_results, awards, photo))
            db.commit()
            print("保存到数据库成功！")
            #cursor.close()
            #db.close()
        except Exception:
            print("save_data_mysql is failed！")
            #db.rollback()
            save_data_mysql(results)



def main():

    # 构造url列表页请求
    for i in range(1,234):
        #time.sleep(4)
        url = "http://139.129.90.206:8040/goods/experts?&current={}&size=10&descs=createTime".format(i)
        print(url)
        # 发送请求，获取每一个专家的id
        ids = parse_expert_id(url)
        # 构造每一个专家的请求
        for id in ids:
            results = parse_expert_details(id)
            # 保存数据到mysql数据库
            if results :
                save_data_mysql(results)



if __name__ == '__main__':
    main()

