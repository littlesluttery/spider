#-*- coding=utf-8 -*-
#@Time : 2020/9/30 10:35 AM
#@Author : 小邋遢
#@File : shenyang_policy_spider.py
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
    url = "http://kjj.shenyang.gov.cn/kxjsj/zwgk/zcfg/glist.html"
    r = requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            html = etree.HTML(r.text)
            total_page_number = html.xpath("//div[@class='right-wrp']/text()")
            total_page_number = ''.join(total_page_number).strip()
            total_page_number = re.split(',',total_page_number)[0][-3]
            return total_page_number
        else:
            return None
    except ConnectionError:
        print("Error of parsing the total number of pages")


def page_urls(url):
    r = requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            html = etree.HTML(r.text)
            urls = html.xpath("//ul[@class='list22']/li/a/@href")
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
        details = ''.join(details)
        original_link = results['original_link']
        try:
            sql = 'insert into policy(title,release_data,source,details,original_link) values(%s,%s,%s,%s,%s)'
            cursor.execute(sql, (title,release_data,source,details,original_link))
            db.commit()
            print("保存到数据库成功.....")
            cursor.close()
            db.close()

        except:
            save_to_mysql(results)
            print('保存到数据库失败.....')




def page_details(url):
    r = requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            print("正在抓取数据......")
            html = etree.HTML(r.text)
            # 标题
            title = html.xpath("//div[@class='cent-title111']/text()")
            title = ''.join(title).strip()

            data =  html.xpath("//div[@class='cent-time111']/text()")
            data = ''.join(data).strip()
            # 发布日期：release_data
            release_data = re.findall("^发布日期：(\d+年\d+月\d+日)",data)
            release_data = ''.join(release_data)
            # 来源
            source = re.findall("来源：(.*)",data)
            source = ''.join(source)
            source = re.split(r"\u3000",source)[0]
            # 内容为图像，保存图像的url
            details = html.xpath("//div[@class='cent-center111']/p//img/@src")
            details = ["http://kjj.shenyang.gov.cn" + i for i in details]
            # 链接
            original_link = html.xpath("//div[@class='cent-center111']/p/a/@href")
            original_link = ''.join(original_link)
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
    for i in range(int(total_page_number)+1):
        if i == 0:
            url = "http://kjj.shenyang.gov.cn/kxjsj/zwgk/zcfg/glist.html"
        else:
            url = "http://kjj.shenyang.gov.cn/kxjsj/zwgk/zcfg/glist{}.html".format(i)
        urls = page_urls(url)
        for url in urls:
            url = "http://kjj.shenyang.gov.cn" + url

            page_details(url)



if __name__ == '__main__':
    main()