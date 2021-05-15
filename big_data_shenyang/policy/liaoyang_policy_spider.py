#-*- coding=utf-8 -*-
#@Time : 2020/10/9 9:42 PM
#@Author : 小邋遢
#@File : liaoning_policy_spider.py
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
    url = "http://kjj.liaoyang.gov.cn/lyskjxxw/xxgk/zcfg/glist.html"
    r = requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            r.encoding='utf-8'
            html = etree.HTML(r.text)
            total_page_number = html.xpath("//div[@class='page-more']/text()")
            total_page_number = ''.join(total_page_number).strip()
            total_page_number = re.findall("当前第 1/(\d+) 页",total_page_number)
            total_page_number = ''.join(total_page_number)
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
            urls = html.xpath("//div[@class='page-list']/ul/li/a/@href")
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
            title = html.xpath("//h2[@class='page-title']/text()")
            title = ''.join(title).strip()


            # 发布日期：release_data
            release_data = html.xpath("//div[@class='fl']/span/text()")
            release_data = ''.join(release_data).strip()
            release_data = re.findall("(\d+-\d+-\d+)",release_data)
            release_data = ''.join(release_data).strip()
            # 来源
            source = html.xpath("//div[@class='fl']/text()")
            source = ''.join(source).strip()
            source = re.findall("文章来源: (.*)", source)
            source = ''.join(source).strip()

            # 内容
            if html.xpath("//div[@id='zoom']/center/a/@href"):
                details = html.xpath("//div[@id='zoom']/center/a/@href")
                details = ''.join(details)
                details = 'http://kjj.liaoyang.gov.cn/' + details

            else:
                details = html.xpath("//div[@id='zoom']//text()")
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
    for i in range(int(total_page_number)+1):
        if i == 0:
            url = "http://kjj.liaoyang.gov.cn/lyskjxxw/xxgk/zcfg/glist.html"
        else:
            url = "http://kjj.liaoyang.gov.cn/lyskjxxw/xxgk/zcfg/glist{}.html".format(i)
        urls = page_urls(url)
        for url in urls:
            url = 'http://kjj.liaoyang.gov.cn/' + url

            page_details(url)



if __name__ == '__main__':
    main()