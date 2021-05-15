#-*- coding=utf-8 -*-
#@Time : 2020/9/30 6:32 PM
#@Author : 小邋遢
#@File : technological_achievements_spider.py
#@Software : PyCharm
'''
科技成果的爬虫
url：https://www.1633.com/tec/
'''
import json
import os
import pymysql
import requests
from lxml import etree
from urllib.request import urlretrieve
import pandas as pd
from technological_achievements.config import *
from urllib.parse import urljoin


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "upgrade-insecure-requests": "1",
    "cookie": "visitor_type=new; 53gid2=10410104288011; 53gid0=10410104288011; 53gid1=10410104288011; visitor_type=new; 53uvid=1; onliner_zdfq61423570=0; 53gid2=10410032576011; 53gid0=10410032576011; 53gid1=10410032576011; KLOG_UID=5G4L2HDAANBEPDBMJ320JKM5FO0VGMCV; Hm_lvt_bb9aa9840c5b6af6a9508300fc5ea0ad=1601214223,1603350111; 53revisit=1603350111161; 53kf_61423570_from_host=www.1633.com; 53kf_61423570_land_page=https%253A%252F%252Fwww.1633.com%252Ftec%252F; kf_61423570_land_page_ok=1; ASP.NET_SessionId=jjr4j5hetznaxobqg2l5yf13; 53kf_61423570_keyword=https%3A%2F%2Fwww.1633.com%2Ftec%2F; acw_tc=1bdd1e1e16033558776952935e93b420dea39569224d0a22947a2c8c97; Hm_lpvt_bb9aa9840c5b6af6a9508300fc5ea0ad=1603355967; reward_time=155"

}
def total_page_numbers(url):
    r = requests.get(url,headers=headers)
    print(r.status_code)
    try:
        if r.status_code == 200:
            html = etree.HTML(r.text)
            a = html.xpath("//div[@class='page']/a/text()")
            if a :
                total_page_number = a[-1]
                return total_page_number
            else:
                return None
        else:
            return None
    except ConnectionError:
        print("Error of parsing the total number of pages")


def page_url(url):
    r = requests.get(url,headers)
    try:

        if r.status_code == 200:
            html = etree.HTML(r.text)
            if html.xpath("//div[@class='teclist']//li/div/h2/a/@href"):
                print(111)
                urls = html.xpath("//div[@class='teclist']//li/div/h2/a/@href")
            else:
                print(222)
                urls = html.xpath("//div[@class='teclist']//li//h2/a/@href")
            # owner：所有人
            owners = html.xpath("//div[@class='teclist']//a[@class='fl']/text()")

            return urls,owners
        else:
            return None,None
    except ConnectionError:
        print("Error of parse page ulr")



def parse_details(data):
    url = data.get('url')
    print(url)
    owner = data.get('owner')
    r = requests.get(url,headers)
    try:
        if r.status_code == 200:
            html = etree.HTML(r.text)
            # achievement_name:成果名称
            achievement_name = html.xpath("//div[@class='detail-top-rt']/h3/span/text()")
            achievement_name = ''.join(achievement_name).strip()
            # application_number:专利申请号
            application_number = html.xpath("//ul[@class='clearfix'][1]/li[1]/text()")
            application_number = ''.join(application_number).split("：")[1].strip()
            # patent_type:专利类型
            patent_type = html.xpath("//ul[@class='clearfix'][1]/li[2]/text()")
            patent_type = ''.join(patent_type).split("：")[1].strip()
            # source:来源
            source = html.xpath("//ul[@class='clearfix'][1]/li[3]/text()")
            source = ''.join(source).split("：")[1].strip()
            # location:所在地
            location = html.xpath("//ul[@class='clearfix'][1]/li[4]/text()")
            location = ''.join(location).split("：")[1].strip()
            # industry:行业
            industry = html.xpath("//ul[@class='clearfix'][1]/li[5]/text()")
            industry = ''.join(industry).split("：")[1].strip()
            # technology_maturit:技术成熟度
            technology_maturity = html.xpath("//ul[@class='clearfix'][2]/li[1]/text()")
            technology_maturity = ''.join(technology_maturity).split("：")[1].strip()
            # last_update_date:最近更新
            last_update_date = html.xpath("//ul[@class='clearfix'][2]/li[2]/text()")
            last_update_date = ''.join(last_update_date).split("：")[1].strip()
            # application_filed:应用领域
            application_filed = html.xpath("//ul[@class='clearfix'][2]/li[3]/text()")
            application_filed = ''.join(application_filed).split("：")[1].strip()
            # project_description:项目简介
            if html.xpath("//div[@class='content']//text()"):
                project_description = html.xpath("//div[@class='content']//text()")
                project_description = ''.join(project_description).strip()
            else:
                project_description = None
            # image:图片
            if html.xpath("//div[@class='smallImg']/span/text()"):
               image_url = html.xpath("//div[@class='smallImg']/span/text()")
               try:
                   print(image_url)
                   url = "".join(image_url)
                   url = json.loads(url)
                   url = url[0]
                   url = url["url"]
                   #img = "https://upload.1633.com/" + url
                   img = urljoin("https://upload.1633.com/",url)
               except:
                   img = None
            else:
                img = None





            results = {
                "achievement_name":achievement_name,
                "application_number":application_number,
                "patent_type":patent_type,
                "source":source,
                "location":location,
                "industry":industry,
                "technology_maturity":technology_maturity,
                "last_update_date":last_update_date,
                "application_filed":application_filed,
                "project_description":project_description,
                "image":img,
                "owner":owner,

            }

            print(results)
            return results

        else:
            return None
    except ConnectionError:
        print("Error of parse details")


def coonect_mysql():

    db = pymysql.connect(**CONFIG)
    cursor = db.cursor()
    return db,cursor

def id_is(achievement_name):
    db, cursor = coonect_mysql()
    # 判断数据是否存在
    sql = 'select achievement_name from technological_achievements where achievement_name="{}"'.format(achievement_name)
    data = pd.read_sql_query(sql, db)
    if len(data["achievement_name"]) != 0:
        print("该科技成果已经存在数据库....")
        cursor.close()
        db.close()
        return 1
    else:
        cursor.close()
        db.close()
        return 0


def save_to_mysql(results):
    db, cursor = coonect_mysql()

    achievement_name = results['achievement_name']
    #判断是否在数据库中，利用成果名称来判断
    flag = id_is(achievement_name)

    if flag==0:

        application_number = results['application_number']
        patent_type = results['patent_type']
        source = results['source']
        location = results['location']
        industry = results['industry']
        technology_maturity = results['technology_maturity']
        last_update_date = results['last_update_date']
        application_filed = results['application_filed']
        project_description = results['project_description']
        image = results['image']
        owner = results['owner']
        #print(achievement_name,owner)

        sql = 'insert into technological_achievements(achievement_name,application_number,patent_type,source,location,industry,technology_maturity,last_update_date,application_filed,project_description,image,owner) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql,(achievement_name,application_number,patent_type,source,location,industry,technology_maturity,last_update_date,application_filed,project_description,image,owner))
            db.commit()
            print("保存到数据库成功！")
            cursor.close()
            db.close()
        except Exception:
            print("save_data_mysql is failed！")
            db.rollback()
            save_to_mysql(results)

def main():
    # 获取每一个分类的url
    for url in URLS:
        print(url)

        # 获取总页数
        total_page_number = total_page_numbers(url)
        if total_page_number:
            # 构造索引页
            print(total_page_number)
            for i in range(1, int(total_page_number) + 1):
                url_list = "{}{}/".format(url, i)
                print(url_list)
                # 抓取每一页url
                urls, owners = page_url(url_list)
                if urls != None:
                    for i in range(len(urls)):
                        data = {
                            "url": "https:" + urls[i],
                            "owner": owners[i]
                        }
                        # print(data)
                        # 提取详细信息
                        results = parse_details(data)
                        if results:
                            # 保存到数据库
                            save_to_mysql(results)
        else:
            try:
                urls, owners = page_url(url)
                print(urls)
                for i in range(len(urls)):
                    data = {
                        "url": "https:" + urls[i],
                        "owner": owners[i]
                    }
                    # print(data)
                    # 提取详细信息
                    results = parse_details(data)
                    if results:
                        # 保存到数据库
                        save_to_mysql(results)
            except:
                pass



if __name__ == '__main__':
    main()