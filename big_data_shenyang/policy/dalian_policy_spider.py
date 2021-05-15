#-*- coding=utf-8 -*-
#@Time : 2020/9/30 12:41 PM
#@Author : 小邋遢
#@File : dalian_policy_spider.py
#@Software : PyCharm

import requests
import re
from lxml import etree
import pymysql
from policy.config import *
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"

}
def total_page_numbers():
    url = "http://www.kjj.dl.gov.cn/government/PublicList?type=1"
    r = requests.get(url,headers)
    try:
        if r.status_code == 200:
            html = etree.HTML(r.text)
            total_page_number = html.xpath("//div[@class='list_2_2_3']/div/text()")
            total_page_number = ''.join(total_page_number).strip()
            total_page_number = total_page_number.split(',')[0]
            total_page_number = re.findall("共 (\d+) 页",total_page_number)
            total_page_number = ''.join(total_page_number)
            return total_page_number

        else:
            return None
    except ConnectionError:
        print("Error of parsing the total number of pages")


def page_urls(url):
    r = requests.get(url,headers)
    try:
        if r.status_code == 200:
            html = etree.HTML(r.text)
            urls = html.xpath("//li[@class='results_list_2 kj-new-list_2_2']/a[1]/@href")
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
    # 判断是否已经存在
    flag = id_is(title)
    if flag == 0:
        print('正在保存到数据库.......')
        release_data = results['release_data']
        details = results['details']
        original_link = results['original_link']
        annex = results['annex']
        try:
            sql = 'insert into policy(title,release_data,details,original_link,annex) values (%s,%s,%s,%s,%s)'
            cursor.execute(sql,(title,release_data,details,original_link,annex))
            db.commit()
            print("保存到数据库成功.....")
            cursor.close()
            db.close()
        except:
            print("保存到数据库失败.....")



def parse_details(url):
    r = requests.get(url,headers)
    try:
        if r.status_code == 200:
            html = etree.HTML(r.text)
            print("正在抓取政策内容.......")
            # 标题
            title = html.xpath("//div[@class='list_details_2_2_1']/text()")
            title = ''.join(title).strip()
            # 发布日期
            release_data = html.xpath("//span[@class='results_details_1_1'][1]/text()")
            release_data = ''.join(release_data).strip()
            release_data = re.findall("^发布日期:(\d+-\d+-\d+)", release_data)
            release_data = ''.join(release_data)
            # 内容
            details = html.xpath("//div[@class='results_details_2 kj-new_1']//p/text()")
            details = ''.join(details).strip()
            # 原文链接
            original_link = html.xpath("//div[@class='results_details_2 kj-new_1']/p/a/@href")
            original_link = ''.join(original_link)
            # 附件
            annex = html.xpath("//a[@class='r']/@href")
            annex = ''.join(annex)
            annex = "http://www.kjj.dl.gov.cn" + annex
            results = {
                "title":title,
                "release_data":release_data,
                'details':details,
                "original_link":original_link,
                "annex":annex,
            }
            print(results)
            save_to_mysql(results)

        else:
           pass
    except ConnectionError:
        print(" Error of parsing page details")




def main():
    # 获取总页数
    total_page_number = total_page_numbers()
    # 构造索引页
    for i in range(1,int(total_page_number)+1):
        url = "http://www.kjj.dl.gov.cn/government/PublicList?page={}&type=1".format(i)
        # 发送请求，拿到每一页的url
        urls = page_urls(url)
        for url in urls:
            url = "http://www.kjj.dl.gov.cn" + url
            # 发送请求，拿到详情页数据
            parse_details(url)


if __name__ == '__main__':
    main()