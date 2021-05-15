#-*- coding=utf-8 -*-
#@Time : 2020/10/9 8:40 PM
#@Author : 小邋遢
#@File : dandong_policy_spider.py
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
    url = "http://ddkjj.dandong.gov.cn/webfile/zcfg/index.html"
    r = requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            r.encoding = 'utf-8'
            html = etree.HTML(r.text)
            total_page_number = html.xpath("//div[@class='foot_list']/a/text()")

            total_page_number = total_page_number[-3]
            total_page_number = ''.join(total_page_number).strip()
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
            urls = html.xpath("//div[@class='frame_list01']/ul/li/a/@href")
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
        source = results['source']
        details = results['details']
        original_link = results['original_link']
        try:
            sql = 'insert into policy(title,release_data,source,details,original_link) values(%s,%s,%s,%s,%s)'
            cursor.execute(sql, (title,release_data,source,details,original_link))
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
            r.encoding = 'utf-8'
            print("正在抓取数据......")
            html = etree.HTML(r.text)
            # 标题
            title = html.xpath("//div[@id='ivs_title']//text()")
            title = ''.join(title).strip()

            data =  html.xpath("//div[@class='read color02']//text()")
            data = ''.join(data).strip()

            # 发布日期：release_data
            release_data = re.findall("发布日期： (.*)", data)
            release_data = ''.join(release_data)
            # 来源
            source = re.findall("信息来源：(.*) ", data)
            source = ''.join(source)
            source = re.split(r"\u3000\u3000", source)[0]

            try:
                # 内容
                details = html.xpath("//div[@class='article_cont']//text()")
                details = ''.join(details)
            except:
                details = None

            # 链接
            original_link = html.xpath("//div[@class='article_cont']/p/a/@href")
            if original_link:
                original_link = ''.join(original_link)
                original_link = 'http:' + original_link
            else:
                original_link = None
            results = {
                "title":title,
                "release_data":release_data,
                "source":source,
                "details":details,
                "original_link":original_link,
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
        if i == 1:
            url = "http://ddkjj.dandong.gov.cn/webfile/zcfg/index.html"
        else:
            url = "http://ddkjj.dandong.gov.cn/webfile/zcfg/index_{}.html".format(i)
        urls = page_urls(url)
        for url in urls:
            url = "http:" + url
            page_details(url)



if __name__ == '__main__':
    main()