#-*- coding=utf-8 -*-
#@Time : 2020/10/29 1:47 PM
#@Author : 小邋遢
#@File : save_company_mysql.py
#@Software : PyCharm


'''
将csv文件中的数据写入数据库表中
'''

import pymysql
import csv
import codecs


def get_conn():
    db = pymysql.connect(host="127.0.0.1", port=3306,
                         user="root", password="671203",
                         db="big_data_shenyang", charset="utf8")
    return db


def insert(cur, sql, args):
    try:
        cur.execute(sql, args)
    except Exception as e:
        print(e)



def read_csv_to_mysql(filename):
    with codecs.open(filename=filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        head = next(reader)
        print(head)
        conn = get_conn()
        cur = conn.cursor()
        sql = 'insert into company_info values(%s,%s,%s,%s,%s,%s,%s)'
        for item in reader:
            args = tuple(item)
            print(args)
            insert(cur, sql=sql, args=args)

        conn.commit()
        cur.close()
        conn.close()


if __name__ == '__main__':
    read_csv_to_mysql(r"/Users/qinlong/PycharmProjects/big_data_shenyang/辽宁大数据项目资料/5215家企业分领域归类-归类等级技术领域3级/company_info.csv")
