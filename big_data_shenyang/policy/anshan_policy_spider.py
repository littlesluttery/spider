#-*- coding=utf-8 -*-
#@Time : 2020/10/9 7:33 PM
#@Author : 小邋遢
#@File : anshan_policy_spider.py
#@Software : PyCharm
import re

import pymysql
import requests
from policy.config import *
from lxml import etree
import pandas as pd


def parse_page_url():
    url = "http://kjj.anshan.gov.cn/asskjj/zwgk/scxx/glist.html"
    r = requests.get(url,headers=HEADERS)
    if r.status_code == 200:
        html = etree.HTML(r.text)
        urls = html.xpath("//div[@class='info']/ul/li/div[2]/a/@href")
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
        source = results['source']

        author = results['author']
        details = results['details']
        original_link = results['original_link']
        try:
            sql = 'insert into policy(title,release_data,source,author,details,original_link) values (%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(title,release_data,source,author,details,original_link))
            db.commit()
            print("保存到数据库成功.....")
            cursor.close()
            db.close()
        except:
            save_to_mysql(results)
            print("保存到数据库失败.....")



def parse_details(url):
    r = requests.get(url,headers=HEADERS)
    if r.status_code == 200:
        html = etree.HTML(r.text)
        # 标题
        title = html.xpath("//div[@class='info hwq-info-article']/ul/div/div[1]//text()")
        title = ''.join(title).strip()
        # 发布日期
        release_data = html.xpath("//div[@class='info hwq-info-article']/ul/div/div[2]/span[1]/text()")
        release_data = ''.join(release_data).strip()
        release_data = re.findall("时间：(.*)",release_data)
        release_data = ''.join(release_data)
        # 来源
        source = html.xpath("//div[@class='info hwq-info-article']/ul/div/div[2]/span[2]/text()")
        source = ''.join(source).strip()
        source = re.findall("来源：(.*)",source)
        source = ''.join(source)
        # 作者
        author = html.xpath("//div[@class='info hwq-info-article']/ul/div/div[2]/span[3]/text()")
        author = ''.join(author).strip()
        author = re.findall("作者：(.*)",author)
        author = ''.join(author)

        # 内容
        if html.xpath("//td[@class='news_font']/div//p/span//text()"):
            details = html.xpath("//td[@class='news_font']/div//p/span//text()")

        else:
            details = html.xpath("//div[@class='hwq-info-article-center']//p//text()")
        details = ''.join(details).strip()
        # 原文链接
        original_link = html.xpath("//a[@class='aa']/@href")
        #original_link = ''.join(original_link)
        original_link = [re.sub("\r\n","",i)for i in original_link]
        original_link = ''.join(original_link).strip()

        results = {
            "title":title,
            "release_data":release_data,
            "source":source,
            "author":author,

            "details":details,
            "original_link":original_link,
        }
        print(results)

        save_to_mysql(results)


    else:
        print("解析详情页内容出错.....")


def run():
    # 获取所有详情页url
    urls = parse_page_url()
    for url in urls:
        # 解析详情页信息
        parse_details(url)


if __name__ == '__main__':
    run()