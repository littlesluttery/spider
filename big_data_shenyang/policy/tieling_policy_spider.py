#-*- coding=utf-8 -*-
#@Time : 2020/10/10 10:50 AM
#@Author : 小邋遢
#@File : tieling_policy_spider.py
#@Software : PyCharm


import pymysql
import requests
import re

from lxml import etree
import pandas as pd

from policy.config import *
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"

}

def total_page_numbers():
    url = "http://www.tieling.gov.cn/tieling/zwgk62/xzqlgk94/skxjsj/index.html"
    r = requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            r.encoding='utf-8'
            html = etree.HTML(r.text)
            total_page_number = html.xpath("//div[@class='easysite-page-wrap']/span//text()")
            total_page_number = ''.join(total_page_number).strip()
            total_page_number = re.findall("当前页:1/(\d+)跳转至",total_page_number)
            total_page_number = ''.join(total_page_number)
            print(total_page_number)
            return total_page_number
        else:
            return None
    except ConnectionError:
        print("Error of parsing the total number of pages")


def page_urls(url):
    r = requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            r.encoding = 'utf-8'
            html = etree.HTML(r.text)
            urls = html.xpath("//div[@class='xzqlml']/a/@href")
            return urls
        else:
            return None
    except ConnectionError:
        print("Error of parsing each page URL")

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
        print("正在保存数据.....")
        release_data = results['release_data']
        details = results['details']
        source = results['source']

        try:
            sql = 'insert into policy(title,release_data,details,source) values(%s,%s,%s,%s)'
            cursor.execute(sql, (title,release_data,details,source))
            db.commit()
            print("保存到数据库成功.....")
            cursor.close()
            db.close()

        except:
            print('保存到数据库失败.....')




def page_details(url):
    r = requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            print("正在抓取数据......")
            r.encoding = 'utf-8'
            html = etree.HTML(r.text)
            # 标题
            title = html.xpath("//div[@class='content']/h1/text()")
            title = ''.join(title).strip()


            # 发布日期：release_data
            release_data = html.xpath("//div[@class='content_source']/span[2]/text()")
            release_data = ''.join(release_data).strip()
            release_data = re.findall("(\d+年\d+月\d+日)",release_data)
            release_data = ''.join(release_data).strip()
            # 来源
            source = html.xpath("//div[@class='content_source']/span[1]/text()")
            source = ''.join(source).strip()
            source = re.findall("文章来源: (.*)", source)
            source = ''.join(source).strip()

            # 内容
            if html.xpath("//div[@class='content_con']/img/@src"):
                details = html.xpath("//div[@class='content_con']/img/@src")
                details = ''.join(details)
                details = 'http://www.tieling.gov.cn' + details

            else:
                details = html.xpath("//div[@id='content_con']//text()")
                details = ''.join(details).strip()

            results = {
                "title":title,
                "release_data":release_data,
                "source":source,
                "details":details,

            }
            print(results)
            save_to_mysql(results)

        else:
            return None
    except ConnectionError:
        print(" Error of parsing img url ")



def main():
    # 获取总页数
    total_page_number = total_page_numbers()

    for i in range(1,int(total_page_number)+1):
        url = 'http://www.tieling.gov.cn/tieling/zwgk62/xzqlgk94/skxjsj/c0a93305-{}.html'.format(i)
        urls = page_urls(url)
        for url in urls:
            url = 'http://www.tieling.gov.cn' + url
            page_details(url)



if __name__ == '__main__':
    main()

