#-*- coding=utf-8 -*-
#@Time : 2020/10/18 7:57 PM
#@Author : 小邋遢
#@File : yingkou_policy_spider.py
#@Software : PyCharm
import re

import pymysql
import requests
import json
from lxml import etree
from policy.config import *
import pandas as pd


def parse_page_url(i):
    url = 'http://kjj.yingkou.gov.cn/EWB_YK_Mid/rest/lightfrontaction/getgovinfolist'
    data = {"token":"","params":{"deptcode":"","categorynum":"003004","pageIndex":i,"pageSize":15,"siteGuid":"befc62b3-fa6f-4ce8-829f-16d7d567773a"}}
    headers = {
        "Referer": "http://kjj.yingkou.gov.cn/dynamic/zw/openlist.html?categorynum=003004",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        "Content-Type": "application/json"
    }
    r = requests.post(url=url,headers=headers,data=json.dumps(data))
    if r.status_code == 200:

        data = json.loads(r.text)

        data = data['custom']
        data = data['data']
        #print(data)
        urls = []
        for j in range(len(data)):
            url = data[j]['infourl']
            if str.endswith(url,'htm') or str.endswith(url,'.pdf'):
                pass
            else:
                if str.startswith(url,"http"):
                    url = url
                    urls.append(url)
                else:
                    url = "http://kjj.yingkou.gov.cn" + url
                    urls.append(url)
    return urls

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
    print(flag)
    if flag == 0:
        release_data = results['release_data']
        index_number = results['index_number']
        issuing_authority = results['issuing_authority']
        data_of_writing = results['data_of_writing']
        subject_heading = results['subject_heading']
        subject_classification = results['subject_classification']
        details = results['details']
        text_number = results['text_number']
        try:
            sql = 'insert into policy(title,release_data,index_number,issuing_authority,data_of_writing,subject_heading,subject_classification,details,text_number) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(title,release_data,index_number,issuing_authority,data_of_writing,subject_heading,subject_classification,details,text_number))
            db.commit()
            print("保存到数据库成功.....")
            cursor.close()
            db.close()
        except:
            save_to_mysql(results)
            print("保存到数据库失败.....")

def parse_page_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",

    }
    try:
        r = requests.get(url,headers=headers)
        if r.status_code == 200:

            html = etree.HTML(r.content.decode())

            # 标题
            if html.xpath("//h3[@id='ivs_title']/text()"):
                title = html.xpath("//h3[@id='ivs_title']/text()")
            else:
                if html.xpath("//td[@colspan='3']/text()"):

                    title = html.xpath("//td[@colspan='3']/text()")
                else:
                    title = html.xpath("//div[@class='con_t']/span/text()")

            title = ''.join(title).strip()

            # 索引号
            if html.xpath("//div[@class='xxgk_detail_head']//tr[2]/td[2]/text()"):
                index_number = html.xpath("//div[@class='xxgk_detail_head']//tr[2]/td[2]/text()")
            else:
                index_number = html.xpath("//b[text()='索  引  号：']/../following-sibling::td[1]/text()")
            index_number = ''.join(index_number).strip()

            # 发文机关
            if html.xpath("//ul[@class='ewb-article-list clearfix']/li[1]/p/text()"):
                issuing_authority = html.xpath("//ul[@class='ewb-article-list clearfix']/li[1]/p/text()")
                issuing_authority = ''.join(issuing_authority).strip()
                issuing_authority = re.findall('发布机构：(.*)', issuing_authority)
            else:
                if html.xpath("//div[@class='xxgk_detail_head']//tr[2]/td[4]/text()"):
                    issuing_authority = html.xpath("//div[@class='xxgk_detail_head']//tr[2]/td[4]/text()")
                else:
                    issuing_authority = html.xpath("//b[text()='发文机关：']/../following-sibling::td[1]/text()")

            issuing_authority = ''.join(issuing_authority).strip()

            # 发布日期
            if html.xpath("//ul[@class='ewb-article-list clearfix']/li[2]/p/text()"):
                release_data = html.xpath("//ul[@class='ewb-article-list clearfix']/li[2]/p/text()")
                release_data = ''.join(release_data)
                release_data = re.findall("发布日期：(.*)", release_data)
            else:
                if html.xpath("//div[@class='xxgk_detail_head']//tr[3]/td[4]/text()"):
                    release_data = html.xpath("//div[@class='xxgk_detail_head']//tr[3]/td[4]/text()")
                else:
                    release_data = html.xpath("//b[text()='发布日期：']/../following-sibling::td[1]/text()")

            release_data = ''.join(release_data).strip()

            # 成文日期
            if html.xpath("//ul[@class='ewb-article-list clearfix']/li[3]/p/text()"):
                data_of_writing = html.xpath("//ul[@class='ewb-article-list clearfix']/li[3]/p/text()")
                data_of_writing = ''.join(data_of_writing)
                data_of_writing = re.findall("成文日期：(.*)", data_of_writing)
            else:
                if html.xpath("//div[@class='xxgk_detail_head']//tr[3]/td[2]/text()"):
                    data_of_writing = html.xpath("//div[@class='xxgk_detail_head']//tr[3]/td[2]/text()")
                else:
                    data_of_writing = html.xpath("//b[text()='成文日期：']/../following-sibling::td[1]/text()")

            data_of_writing = ''.join(data_of_writing).strip()

            # 发文字号
            if html.xpath("//ul[@class='ewb-article-list clearfix']/li[4]/p/text()"):
                text_number = html.xpath("//ul[@class='ewb-article-list clearfix']/li[4]/p/text()")
                text_number = ''.join(text_number)
                text_number = re.findall("发文字号：(.*)", text_number)
            else:
                if html.xpath("//div[@class='xxgk_detail_head']//tr[4]/td[2]/text()"):
                    text_number = html.xpath("//div[@class='xxgk_detail_head']//tr[4]/td[2]/text()")
                else:
                    text_number = html.xpath("//b[text()='发文字号：']/../following-sibling::td[1]/text()")

            text_number = ''.join(text_number).strip()

            # 主题词
            subject_heading = html.xpath("//b[text()='主  题  词：']/../following-sibling::td[1]/text()")
            subject_heading = ''.join(subject_heading)

            # 主题分类
            if html.xpath("//ul[@class='ewb-article-list clearfix']/li[5]/p/text()"):

                subject_classification = html.xpath("//ul[@class='ewb-article-list clearfix']/li[5]/p/text()")
                subject_classification = ''.join(subject_classification)
                subject_classification = re.findall("主题分类：(.*)", subject_classification)
            else:
                subject_classification = html.xpath("//b[text()='主题分类：']/../following-sibling::td[1]/text()")

            subject_classification = ''.join(subject_classification).strip()
            # 内容
            if len(html.xpath("//div[@id='ivs_content']/p/img/@src"))>1:

                details = html.xpath("//div[@id='ivs_content']/p/img/@src")
                details = ["http://kjj.yingkou.gov.cn" + i for i in details]

            else:
                if html.xpath("//div[@id='Zoom']//p//text()"):

                    details = html.xpath("//div[@id='Zoom']//p//text()")
                else:
                    if html.xpath("//div[@id='ivs_content']//p//text()"):

                        details = html.xpath("//div[@id='ivs_content']//p//text()")
                    else:

                        if html.xpath("//td[@class='b12c']//p//text()"):
                            details = html.xpath("//td[@class='b12c']//p//text()")
                        else:
                            details = html.xpath("//div[@id='fontzoom']/p/text()")


            details = ''.join(details).strip()

            results = {
            "url":url,
            "title":title,
            "index_number":index_number,
            "issuing_authority":issuing_authority,
            "release_data":release_data,
            "data_of_writing":data_of_writing,
            "text_number":text_number,
            "subject_heading":subject_heading,
            "subject_classification":subject_classification,
            "details":details,

            }
            print(results)
            save_to_mysql(results)


    except:
        pass







def run():
    # 构造索引页
    for i in range(7):
        print(i)
        # 发送索引页请求
        urls = parse_page_url(i)
        # 请求详情页
        for url in urls:
            parse_page_details(url)


if __name__ == '__main__':
    run()