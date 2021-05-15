#-*- coding=utf-8 -*-
#@Time : 2020/10/16 11:35 AM
#@Author : 小邋遢
#@File : cookies.py
#@Software : PyCharm



import pytesseract
import requests
headers = {

    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}


def parse_code():
    text = pytesseract.image_to_string("1.png")
    return text


def get_img(s):
    #img_url = 'http://218.60.146.4/pubsearch/portal/login-showPic.shtml'
    img_url = 'http://218.60.146.4:80/pubsearch/portal/app/uilogin/images/codeCover.jpg?v=20201020'
    r = s.get(url=img_url, headers=headers)

    if r.status_code == 200:
        with open('1.png', 'wb') as f:
            f.write(r.content)
    return s

def get_url_cookies(s,text):

    url = 'http://218.60.146.4/pubsearch/wee/platform/wee_security_check?v=20201020'
    #url = "http://218.60.146.4/pubsearch/portal/keepAlive.shtml"

    headers = {
        "Origin": "http://218.60.146.4",
        "Host": "218.60.146.4",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "http://218.60.146.4/pubsearch/portal/uilogin-forwardLogin.shtml",
        "Upgrade-Insecure-Requests": "1",

        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    data = {
        "j_loginsuccess_url":"",
        "j_validation_code": text,
        "j_username": "bmxwZmZfMTIzNA==",
        "j_password": "bmxwMTJfMzQ=",
    }
    r = s.post(url=url, headers=headers, data=data)
    print(r.text)
    if r.status_code == 200:

        cookies = requests.utils.dict_from_cookiejar(r.cookies)
        # Cookie: IS_LOGIN=false; WEE_SID=E1E565BA3C9ED143A3A6491B6DE188BB.pubsearch05; JSESSIONID=E1E565BA3C9ED143A3A6491B6DE188BB.pubsearch05
        cookies =  "WEE_SID=" + cookies['WEE_SID'] + "; " "IS_LOGIN=" + "true"+  "; "+ "JSESSIONID=" + cookies['WEE_SID']
    return s,cookies

def get_login(s,cookies):
    print(cookies)
    #url = "http://218.60.146.4/pubsearch/portal/portal/uiIndex.shtml"
    url = "http://218.60.146.4/pubsearch/portal/keepAlive.shtml"
    headers = {
        "Connection": "keep-alive",
       "Origin": "http://218.60.146.4",
        "Cookies":cookies,
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "http://218.60.146.4/pubsearch/portal/portal/uiIndex.shtml",
        #"Referer": "http://218.60.146.4/pubsearch/portal/uilogin-forwardLogin.shtml",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
    }
    r = s.get(url=url,headers=headers)
    print(r.text)
    if r.status_code == 200:
        cookies = requests.utils.dict_from_cookiejar(r.cookies)
        #print(cookies)



def start_cookies():
    # 创建会话
    s = requests.Session()
    # 获取照片
    s = get_img(s)
    # parse_code
    text = parse_code()
    # 获取登录状态
    s,cookies = get_url_cookies(s, text)
    # 利用登录状态访问登录页面
    get_login(s,cookies)



if __name__ == '__main__':
    start_cookies()




