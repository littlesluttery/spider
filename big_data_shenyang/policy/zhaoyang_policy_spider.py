#-*- coding=utf-8 -*-
#@Time : 2020/10/10 12:54 PM
#@Author : 小邋遢
#@File : zhaoyang_policy_spider.py
#@Software : PyCharm


#-*- coding=utf-8 -*-
#@Time : 2020/10/10 10:44 AM
#@Author : 小邋遢
#@File : fuxin_policy_spider.py
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



def page_urls(url):
    r = requests.get(url,headers=headers)
    try:
        if r.status_code == 200:
            r.encoding = 'utf-8'
            html = etree.HTML(r.text)
            urls = html.xpath("//div[@class='wb-colu'][1]/div/ul/li/div/a/@href")
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
            title = html.xpath("//p[@class='ewb-con-tt']//text()")
            title = ''.join(title).strip()


            # 发布日期：release_data
            release_data = html.xpath("//p[@class='ewb-con-det']/text()")
            release_data = ''.join(release_data).strip()
            release_data = re.findall("(\d+-\d+-\d+)",release_data)
            release_data = ''.join(release_data).strip()
            # 来源
            source = html.xpath("//p[@class='ewb-con-det']/span/text()")
            source = ''.join(source).strip()
            source = re.findall("来源: (.*)", source)
            source = ''.join(source).strip()

            # 内容
            if html.xpath("//div[@id='Zoom']//p//text()"):
                details = html.xpath("//div[@id='Zoom']//p//text()")
            else:
                details = html.xpath("//div[@class='ewb-con']//text()")
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
        url = 'http://kjj.zgcy.gov.cn/cyskjj/czfg/'
        urls = page_urls(url)
        for url in urls:
            url = 'http://kjj.zgcy.gov.cn' + url
            page_details(url)



if __name__ == '__main__':
    main()