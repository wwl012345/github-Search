import configparser
import os
import re
import traceback
from time import gmtime, sleep, strftime
import requests
from lxml import etree
from tqdm import tqdm
import urllib3
urllib3.disable_warnings()
import urllib.parse

def login_github(username,password):#登陆Github
    #初始化参数
    login_url = 'https://github.com/login'
    session_url = 'https://github.com/session'
    try:
        #获取session
        s = requests.session()
        resp = s.get(login_url).text
        dom_tree = etree.HTML(resp)
        key = dom_tree.xpath('//input[@name="authenticity_token"]/@value')
        user_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': key,
            'login': username,
            'password': password
        }
        #发送数据并登陆
        s.post(session_url,data=user_data)
        return s
    except Exception as e:
        print('产生异常，请检查网络设置及用户名和密码')
        error_Record(str(e), traceback.format_exc())

def hunter(gUser, gPass, keywords):
    global total_codes
    global keyword_Urls
    global name_Spaces
    try:
        #代码搜索
        s = login_github(gUser,gPass)
        r = s.get('https://github.com/session')
        title = re.findall('<title>(.+?)</title>',r.text)
        if title[0] == 'GitHub':
            print('登录成功，正在检索泄露信息.......')
        else:
            print("登录失败，请重试!")
        sleep(1)
        total_codes = []
        keyword_Urls = []
        name_Spaces = []
        #新加入2条正则匹配，第一条匹配搜索出来的代码部分；第二条则进行高亮显示关键词
        pattern_code = re.compile(r'<div class="file-box blob-wrapper my-1">(.*?)</div>', re.S)
        pattern_sub = re.compile(r'''<span class='text-bold'>''', re.S)
        for keyword in keywords:
            for page in tqdm(range(1,7)):
                #更改搜索排序方式的url，收录可能存在泄漏的url还是使用xpath解析
                search_code = 'https://github.com/search?o=desc&p=' + str(page) + '&q=' + keyword +'&s=indexed&type=Code'
                resp = s.get(search_code)
                results_code = resp.text
                dom_tree_code = etree.HTML(results_code)
                #获取存在信息泄露的链接地址
                Urls = dom_tree_code.xpath('//div[@class="f4 text-normal"]/a/@href')
                for url in Urls:
                    url = 'https://github.com' + url
                    keyword_Urls.append(url)
        #打印结果
        for result in keyword_Urls:
            print(result)
    except Exception as e:
        print(e)

def error_Record(error, tb):
    try:
        if os.path.exists('error.txt'):
            with open('error.txt', 'a', encoding='utf-8') as f:
                f.write(strftime("%a, %d %b %Y %H:%M:%S",gmtime()) + "-" + "Exception Record: " + error + '\n' + "具体错误信息如下：\n" +tb + '\r\n')
        else:
            with open('error.txt', 'w', encoding='utf-8') as f:
                f.write(strftime("%a, %d %b %Y %H:%M:%S",gmtime()) + "-" + "Exception Record: " + error + '\n' + "具体错误信息如下：\n" +tb + '\r\n')
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # configparser模块支持读取.conf和.ini等类型的配置文件
    config = configparser.ConfigParser()
    config.read('info.ini', encoding='UTF-8')
    gUser = config['Github']['user']
    gPass = config['Github']['password']
    keywords = []
    keywords_begin = []

    # 组合关键词，keyword + payload,两者之间加入“+”号，符合Github搜索语法
    for keyword in config['KEYWORDS']:
        for payload in config['PAYLOADS']:
            keyword_encode = urllib.parse.quote(config['KEYWORDS'][keyword])
            payload_encode = urllib.parse.quote(config['PAYLOADS'][payload])
            keywords.append(keyword_encode + '+' + payload_encode)
            keywords_begin.append(config['KEYWORDS'][keyword] + '+' + config['PAYLOADS'][payload])
    #total_codes, keyword_Urls, s = hunter(gUser, gPass, keywords)
    hunter(gUser, gPass, keywords)