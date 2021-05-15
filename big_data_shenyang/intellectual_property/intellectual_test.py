#-*- coding=utf-8 -*-
#@Time : 2020/10/7 3:38 PM
#@Author : 小邋遢
#@File : intellectual_test.py
#@Software : PyCharm
import json
import random
import re

import pymysql
from big_data_shenyang.config import CONFIG
from intellectual_property.config import *
import requests
import xmltodict
from lxml import etree
import pandas as pd
from intellectual_property.cookies import *

results = None

# 解析著录项目
def parse_bibliographic_items(vid, id,cookies):
    data = {
        "nrdAn":vid,
        "cid":id,
        "sid":id,
        "wee.bizlog.modulelevel": "0201101",
    }
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    r = requests.post(url=BIBLIOGRAPHIC_ITEMS_URL, headers=headers, data=data)
    if r.status_code == 200:
            data = json.loads(r.text)
            data = data['abstractInfoDTO']
            # 摘要：abstract
            abstract = data['abIndexList']
            abstract = abstract[0]['value']
            abstract = xmltodict.parse(abstract)
            abstract = json.dumps(abstract, ensure_ascii=False)
            abstract = json.loads(abstract)
            if abstract['RESULT']['table']['tr']['td']['business:Abstract']['base:Paragraphs']['#text']:
                abstract = abstract['RESULT']['table']['tr']['td']['business:Abstract']['base:Paragraphs']['#text']
            else:
                abstract = None
            if data['tioIndex']:
                # 专利名称：patent_name
                patent_name = data['tioIndex']
                patent_name = patent_name['value']
            else:
                patent_name = None
            #print(data['abstractItemList'])
            # 申请号：application_number
            text_1 = data['abstractItemList'][0]['indexCnName']
            text_1 = re.sub('&shy;','',text_1)

            if text_1 == '申请号':
                application_number = data['abstractItemList'][0]
                application_number = application_number['value']
            else:
                application_number = None

            # 申请日：application_date
            text_2 = data['abstractItemList'][1]['indexCnName']

            if text_2 == '申请日':
                application_date = data['abstractItemList'][1]
                application_date = application_date['value']
            else:
                application_date = None

            # 公开（公告）号：public_number
            text_3 = data['abstractItemList'][2]['indexCnName']
            text_3 = re.sub('&shy;', '', text_3)

            if text_3 == '公开（公告）号':
                public_number = data['abstractItemList'][2]
                public_number = public_number['value']
            else:
                public_number = None

            # 公开（公告）日：public_date
            text_4 = data['abstractItemList'][3]['indexCnName']

            if text_4 == '公开（公告）日':
                public_date = data['abstractItemList'][3]
                public_date = public_date['value']
            else:
                public_date = None

            # IPC分类号：IPC_classification_number
            text_5 = data['abstractItemList'][4]['indexCnName']

            if text_5 == 'IPC分类号':
                IPC_classification_number = data['abstractItemList'][4]
                IPC_classification_number = IPC_classification_number['value']
            else:
                IPC_classification_number = None

            # 申请（专利权）人：applicant
            text_6 = data['abstractItemList'][5]['indexCnName']

            if text_6 == '申请（专利权）人':
                applicant = data['abstractItemList'][5]
                applicant = applicant['value']
            else:
                applicant = None

            # 发明人：inventor
            text_7 = data['abstractItemList'][6]['indexCnName']

            if text_7 == '发明人':
                inventor = data['abstractItemList'][6]
                inventor = inventor['value']
            else:
                inventor = None

            # 优先权号：priority_number
            text_8 = data['abstractItemList'][7]['indexCnName']

            if text_8 == '优先权号':
                priority_number = data['abstractItemList'][7]
                priority_number = priority_number['value']
            else:
                priority_number = None

            # 优先权日：priority_date
            text_9 = data['abstractItemList'][8]['indexCnName']

            if text_9 == '优先权日' :
                priority_date = data['abstractItemList'][8]
                priority_date = priority_date['value']
            else:
                priority_date = None

            # 申请人地址；applicant_address
            text_10 = data['abstractItemList'][9]['indexCnName']

            if text_10 == '申请人地址':
                applicant_address = data['abstractItemList'][9]
                applicant_address = applicant_address['value']
            else:
                applicant_address = None

            # 申请人邮编：applicant_zip_code
            text_11 = data['abstractItemList'][10]['indexCnName']

            if text_11 == '申请人邮编':
                applicant_zip_code = data['abstractItemList'][10]
                applicant_zip_code = applicant_zip_code['value']
            else:
                applicant_zip_code = None

            # 申请人所在国家（省）：applicant_country
            text_12 = data['abstractItemList'][11]['indexCnName']
            #print(text_12)

            if text_12 == '申请人所在国（省）':

                applicant_country = data['abstractItemList'][11]
                applicant_country = applicant_country['value']
            else:
                applicant_country = None
            print('111111')
            #print(applicant)
            #print(patent_name,abstract,application_number,application_date,public_number,public_date,IPC_classification_number,applicant,inventor,priority_number,priority_date,applicant_address,applicant_zip_code,applicant_country)
            return patent_name, abstract, application_number, application_date, public_number, public_date, IPC_classification_number, applicant, inventor, priority_number, priority_date, applicant_address, applicant_zip_code, applicant_country

    else:
        print('解析著录项目出错......')


# 解析全文文本
def parse_full_text(vid, id, cookies):
    data = {
        "nrdAn": vid,
        "cid": id,
        "sid": id,
    }
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }

    r = requests.post(url=FULL_TEXT_URL, headers=headers, data=data)
    if r.status_code == 200:
        data = json.loads(r.text)
        data = data['fullTextDTO']
        # 权利要求书和说明书：claims---manual
        data = data["literaInfohtml"]
        try:
            html = etree.HTML(data.encode('utf-8'))
            # 权利要求书
            claims = html.xpath("//div[1]/table/tr/td//text()")
            claims = ''.join(claims)

            # 说明书
            manual = html.xpath("//div[2]/table/tr/td//text()")
            manual = ''.join(manual)
            print(222222)
            return claims, manual
        except:
            claims = None
            manual = None
            return claims,manual

    else:
        print('解析全文文本出错.......')


# 解析全文图像
def parse_full_image(vid, cpn, cookies):
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    url = FULL_IMAGE_URL.format(vid,cpn,cpn)
    r = requests.post(url=url, headers=headers)
    if r.status_code == 200:
        print(333333)
    else:
        print("解析全文图像出错....")

# 获取法律状态信息
def parse_legal_status(cpn, vid, cookies):
    data = {
        "lawState.nrdPn": cpn,
        "lawState.nrdAn": vid,
        "wee.bizlog.modulelevel": "0202201",
        "pagination.start": "0",
    }
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }

    r = requests.post(url=LEGAL_STATUS, headers=headers, data=data)
    if r.status_code == 200:
        try:
            data = json.loads(r.text)

            data = data['lawStateList'][0]
            # 法律状态含义
            legal_status_meaning = data['lawStateCNMeaning']
            # 法律状态生效日
            effective_date_legal_status = data['prsDate']
            print(444444)
            return legal_status_meaning ,effective_date_legal_status
        except:
            legal_status_meaning = None
            effective_date_legal_status= None
            return legal_status_meaning, effective_date_legal_status
    else:
        pass


# 获取同族文献和引证文献信息
def parse_literature(vid, cpn, cookies):
    data = {
        "literaInfo.nrdAn": vid,
        "literaInfo.nrdPn": cpn,
        "literaInfo.fn": "",
    }
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }

    r = requests.post(url=LEGAL_STATUS, headers=headers, data=data)
    if r.status_code == 200:
        try:
            data = json.loads(r.text)
            data = data['cognationList'][0]
            # 发明名称：invTitleNO
            invTitleNO = data['invTitleNO']
            # 优先权号：prn
            prn = data['prn']
            # 公开号:pn
            pn = data['pn']
            # 公开日：pubDate
            pubDate = data['pubDate']
            # 申请号：an
            an = data['an']
            print(555555)
            return invTitleNO,prn,pn,pubDate,an
        except:
            invTitleNO = None
            prn = None
            pn = None
            pubDate = None
            an = None
            print("无数据.....")
            return invTitleNO,prn,pn,pubDate,an

    else:
        print('解析同族文献和引证文献信息出错.....')


def parse_page_details(vid, id,cpn,name, cookies):
    flag = id_is('application_number', vid)
    if flag == 0:
        try:
            # 调用著录项目，拿到数据
            patent_name, abstract, application_number, application_date, public_number, public_date, IPC_classification_number, applicant, inventor, priority_number, priority_date, applicant_address, applicant_zip_code, applicant_country = parse_bibliographic_items(
                vid, id, cookies)
            # 调用全文文本，拿到数据
            claims, manual = parse_full_text(vid, id, cookies)
            # 调用全文图像，拿到数据,内容为flash加载，无法处理。
            # parse_full_image(vid, cpn, cookies)
            # 调用法律状态，拿到数据
            legal_status_meaning, effective_date_legal_status = parse_legal_status(cpn, vid, cookies)
            # 调用同族文献和引证文献，拿到数据
            invTitleNO, prn, pn, pubDate, an = parse_literature(vid, cpn, cookies)
            results = {
                "company_name": name,
                "patent_name": patent_name,
                "abstract": abstract,
                "application_number": application_number,
                "application_date": application_date,
                "public_number": public_number,
                "public_date": public_date,
                "IPC_classification_number": IPC_classification_number,
                "applicant": applicant,
                "inventor": inventor,
                "priority_number": priority_number,
                "priority_date": priority_date,
                "applicant_address": applicant_address,
                "applicant_zip_code": applicant_zip_code,
                "applicant_country": applicant_country,
                "claims": claims,
                "manual": manual,
                "legal_status_meaning": legal_status_meaning,
                "effective_date_legal_status": effective_date_legal_status,
                "invTitleNO": invTitleNO,
                "prn": prn,
                "pn": pn,
                "pubDate": pubDate,
                "an": an,

            }
            # print(results)
            # 保存所有数据到数据库
            if results:
                save_to_mysql(results)
        except:
            pass


def next_page_url(dealSearchKeywords, executableSearchExp, literatureSF, totalCount, name, cookies):
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    page_number = totalCount//12+1
    for i in range(1,page_number):
        data = {
            "resultPagination.limit": 12,
            "resultPagination.sumLimit": 10,
            "resultPagination.start": 12*i,
            "resultPagination.totalCount": 146,
            "searchCondition.sortFields": "-APD,+PD",
            "searchCondition.searchType": "Sino_foreign",
            "searchCondition.originalLanguage":"",
            "searchCondition.extendInfo['MODE']": "MODE_SMART",
            "searchCondition.extendInfo['STRATEGY']": "",
            "searchCondition.searchExp": literatureSF,
            "searchCondition.executableSearchExp": executableSearchExp,
            "searchCondition.dbId": "",
            "searchCondition.literatureSF": literatureSF,
            "searchCondition.targetLanguage":"",
            "searchCondition.resultMode": "undefined",
            "searchCondition.strategy": "",
            "searchCondition.searchKeywords":dealSearchKeywords,

        }
        r = requests.post(url=NEXT_UTL, headers=headers, data=data)
        print(r.status_code)
        if r.status_code == 200:
            data = json.loads(r.text)
            data = data['searchResultDTO']
            data_list = data['searchResultRecord']

            for data in data_list:
                data = data['fieldMap']
                # 详情页需要的data
                vid = data['VID']
                id = data["ID"]
                cpn = data['PN_BAK']
                #print(vid, id)
                flag = id_is('application_number', vid)
                if flag == 0:
                    # 抓取详情页的所有数据
                    parse_page_details(vid, id, cpn, name, cookies)





def search_company_name(name,cookies,INDEX_URL):
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }

    data = {
        "searchCondition.searchExp": name,
        "search_scope":"",
        "searchCondition.dbId": "VDB",
        "resultPagination.limit": "12",
        "searchCondition.searchType": "Sino_foreign",
        "wee.bizlog.modulelevel": "0200101",
    }
    r = requests.post(url=INDEX_URL,headers=headers,data=data)
    print(r.status_code)
    if r.status_code == 200:
        data = json.loads(r.text)
        searchResultDTO = data['searchResultDTO']
        data_list = searchResultDTO['searchResultRecord']

        for data_page in data_list:
            data_page = data_page['fieldMap']
            # 详情页需要的data
            vid = data_page['VID']
            id = data_page["ID"]
            cpn = data_page['PN_BAK']
            print(vid, id)
            # 抓取详情页的所有数据
            # 添加判断
            flag = id_is('application_number', vid)
            if flag== 0:
                parse_page_details(vid, id, cpn, name, cookies)
        # 下一页索引页所需的data
        # [大][ ]{0,}[连][ ]{0,}[日][ ]{0,}[佳][ ]{0,}[电][ ]{0,}[子][ ]{0,}[有][ ]{0,}[限][ ]{0,}[公][ ]{0,}[司][ ]{0,}
        dealSearchKeywords = searchResultDTO['dealSearchKeywords']
        dealSearchKeywords = ''.join(dealSearchKeywords)
        # "VDB:(IBI='大连日佳电子有限公司')"
        executableSearchExp = searchResultDTO['executableSearchExp']
        # 复合申请人与发明人=(大连日佳电子有限公司)
        literatureSF = searchResultDTO['literatureSF']
        totalCount = searchResultDTO['pagination']
        totalCount = totalCount['totalCount']
        next_page_url(dealSearchKeywords,executableSearchExp,literatureSF,totalCount,name,cookies)




    else:
        print(1111)

def coonect_mysql():
    db = pymysql.connect(**CONFIG)
    cursor = db.cursor()
    return db, cursor

def update_cookies():
    db,cursor = coonect_mysql()
    sql = 'select cookies from cookies where id=1'
    data = pd.read_sql_query(sql,db)
    cookies = data['cookies'][0]
    return cookies

def id_is(name1,name2):
    db, cursor = coonect_mysql()
    # 判断数据是否存在
    #sql = 'select patent_name from patent where patent_name="{}"'.format(patent_name)
    sql = 'select * from patent where {}="{}"'.format(name1,name2)
    data = pd.read_sql_query(sql, db)
    if len(data["patent_name"]) != 0:
        print("该专利已经存在数据库....")
        cursor.close()
        db.close()
        return 1
    else:
        cursor.close()
        db.close()
        return 0


def save_to_mysql(results):
    db,cursor = coonect_mysql()
    patent_name = results['patent_name']
    # 判断该专利是否在数据库中
    flag = id_is('patent_name',patent_name)
    if flag == 0:
        #print(results)
        company_name = results['company_name']
        application_number = results['application_number']
        application_date = results['application_date']
        public_number = results['public_number']
        public_date = results['public_date']
        IPC_classification_number = results['IPC_classification_number']
        applicant = results['applicant']
        inventor = results['inventor']
        priority_number = results['priority_number']
        priority_date = results['priority_date']
        applicant_address = results['applicant_address']
        applicant_zip_code = results['applicant_zip_code']
        applicant_country = results['applicant_country']
        abstract = results['abstract']
        claims = results['claims']
        manual = results['manual']
        legal_status_meaning = results['legal_status_meaning']
        effective_date_legal_status = results['effective_date_legal_status']
        invTitleNO = results['invTitleNO']
        prn = results['prn']
        pubDate = results['pubDate']
        an = results['an']
        try:
            sql = 'insert into patent(company_name,patent_name,application_number,application_date,public_number,public_date,IPC_classification_number,applicant,inventor,priority_number,priority_date,applicant_address,applicant_zip_code,applicant_country,abstract,claims,manual,legal_status_meaning,effective_date_legal_status,invTitleNO,prn,pubDate,an) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql,(company_name,patent_name,application_number,application_date,public_number,public_date,IPC_classification_number,applicant,inventor,priority_number,priority_date,applicant_address,applicant_zip_code,applicant_country,abstract,claims,manual,legal_status_meaning,effective_date_legal_status,invTitleNO,prn,pubDate,an))
            db.commit()
            print("保存到数据库成功.....")
            cursor.close()
            db.close()


        except:
            print("保存出错....")
            #save_to_mysql(results)
    else:
        print("保存失败......")


def run():
        # 从数据库获取更新的cookies
        cookies = update_cookies()
        #cookies = start_cookies()
        print(cookies)
        for i in range(len(COMPANY_NAME)):
            print(i)
            name = random.choice(COMPANY_NAME)
            name = ''.join(name)
            # 加入判断，该公司是否已经查询过专利数据
            flag = id_is('company_name',name)
            if flag == 0:
                print(name)
                if i % 2000 == 0:
                    cookies = update_cookies()
                else:
                    try:
                        # 根据公司名称进行搜索
                        search_company_name(name, cookies, INDEX_URL)
                        index = COMPANY_NAME.index(name)
                        del COMPANY_NAME[index]
                    except:
                        pass

                # cookies = 'WEE_SID=31AB090EE98F87D48BD2D69167662F0F.pubsearch02; IS_LOGIN=true; JSESSIONID=8B251383E42D2EDA9BD18582A9B6C1C4.pubsearch02; avoid_declare=declare_pass'





if __name__ == '__main__':
    run()