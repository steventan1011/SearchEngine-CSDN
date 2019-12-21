from requests_html import HTMLSession
import requests
import re
import time
import mysql.connector
# from selenium import webdriver

global url_list
url_list = []

def download(url):
    data = {}
    session = HTMLSession()
    try:
        r = session.get(url)
        html = r.html
        data['name'] = html.find('h1.title-article')[0].text
        data['url'] = url
        data['author'] = html.find('a.follow-nickName')[0].text
        data['read_times'] = html.find('span.read-count')[0].text.strip('阅读数：')
        data['uptime'] = html.find('span.time')[0].text
        tags = []
        for i in html.find('a.tag-link'):
            tags.append(i.text)
        if len(tags):
            del tags[-1]
        data['tag'] = '/'.join(tags)
        data['content'] = html.find('div.article_content')[0].text

        urls = []
        for i in html.find('div.recommend-box>div>a'):
            urls.append(i.attrs['href'])
        data['nextURLs'] = '\\'.join(urls)
        connectMYSQL(data)
    except (UnicodeDecodeError, IndexError, TimeoutError) as e:
        print(url)
        print(e)
    except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema) as e:
        print(url)
        print(e)


def connectMYSQL(data):
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute(
            "INSERT INTO Blogs(`blog_name`,`url`,`author`, `read_times`, `uptime`, `tag`, `content`, `nextURLs`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            [data['name'], data['url'], data['author'], data['read_times'], data['uptime'], data['tag'], data['content'], data['nextURLs']])
        print('************** %s 数据保存成功 **************' % data['name'])
        conn.commit()
        cursor.close()
    except (mysql.connector.errors.IntegrityError, mysql.connector.errors.DataError) as e:
        print(e)


def seedSpread(url):
    try:
        cursor = conn.cursor(buffered=True)
        cursor.execute(
            "SELECT `nextURLs` FROM `Blogs` WHERE `url`='%s'" %url)
        spread = cursor.fetchone()
        conn.commit()
        cursor.close()
        spread = str(spread).strip('(').strip(')').strip(',')
        spreads = eval(spread).split('\\')
        for i in spreads:
            if i not in url_list:
                url_list.append(i)
                download(i)
                # time.sleep(1)
    except AttributeError as e:
        print(e)

def wholeDownload(url):
    # 第一条
    url_list.append(url)
    download(url)
    seedSpread(url)
    # 之后的每条
    num = 1
    while True:
        # cursor = conn.cursor(buffered=True)
        # cursor.execute(
        #     "SELECT `url` FROM `Blogs` LIMIT %d, 1" %num)
        # nextURL = cursor.fetchone()
        # nextURL = str(nextURL).strip('(').strip(')').strip(',')
        # nextURL = eval(nextURL)
        # print(nextURL)
        # conn.commit()
        # cursor.close()
        nextURL = url_list[num]
        download(nextURL)
        seedSpread(nextURL)
        num += 1
    print(num)

if __name__ == '__main__':
    conn = mysql.connector.connect(
        user='root',
        password='root',
        host='39.106.197.210',
        port='3306',
        database='CSDN'
    )
    urlSeed = 'https://blog.csdn.net/hixiaoyang/article/details/82777044'
    wholeDownload(urlSeed)
    conn.close()
