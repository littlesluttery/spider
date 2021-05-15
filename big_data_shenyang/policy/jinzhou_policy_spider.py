#-*- coding=utf-8 -*-
#@Time : 2020/10/9 9:12 PM
#@Author : 小邋遢
#@File : jinzhou_policy_spider.py
#@Software : PyCharm

import re

import pymysql
import requests
from policy.config import *
from lxml import etree
import pandas as pd


def parse_page_url():
    url = "http://kjj.jz.gov.cn/new_list.php?cid=155"
    r = requests.get(url,headers=HEADERS)
    if r.status_code == 200:
        html = etree.HTML(r.text)
        urls = html.xpath("//div[@class='frame_list01']/ul/li/a/@href")
        return urls
    else:
        print(" 解析列表页url出错.....")

def coonect_mysql():
    db = pymysql.connect(**CONFIG)
    cursor = db.cursor()
    return db,cursor

def id_is(title):
    db, cursor = coonect_mysql()
    # 判断数据是否存在
    sql = 'select title from policy where title="{}"'.format(title)
    data = pd.read_sql_query(sql, db)

    if len(data["title"]) != 0:
        print("该内容已经存在数据库....")
        return 1
    else:
        return 0

def save_to_mysql(results):
    db,cursor = coonect_mysql()
    title = results['title']
    flag = id_is(title)
    if flag == 0:
        release_data = results['release_data']
        details = results['details']

        try:
            sql = 'insert into policy(title,release_data,details) values (%s,%s,%s)'
            cursor.execute(sql,(title,release_data,details))
            db.commit()
            print("保存到数据库成功.....")
            cursor.close()
            db.close()
        except:
            print("保存到数据库失败.....")



def parse_details(url):
    r = requests.get(url,headers=HEADERS)
    if r.status_code == 200:
        html = etree.HTML(r.text)
        # 标题
        title = html.xpath("//div[@id='ivs_title']/text()")
        title = ''.join(title).strip()
        data = html.xpath("//div[@class='read color02']//text()")
        data = ''.join(data).strip()
        # 发布日期
        release_data = re.findall(" (\d+-\d+\d+)", data)
        release_data = ''.join(release_data)


        # 内容
        details = html.xpath("//div[@class='article_cont']//text()")
        details = ''.join(details).strip()

        results = {
            "title":title,
            "release_data":release_data,
            "details":details,

        }
        print(results)

        save_to_mysql(results)


    else:
        print("解析详情页内容出错.....")


def run():
    # 获取所有详情页url
    urls = parse_page_url()
    for url in urls:
        url = "http://kjj.jz.gov.cn/"+ url
        # 解析详情页信息
        parse_details(url)


if __name__ == '__main__':
    run()