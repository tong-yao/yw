# -*- coding=utf-8 -*-
# @Time : 2019/6/25 16:16 
# @Author : piller
# @File : settings.py 
# @Software: PyCharm
import requests
from fake_useragent import UserAgent
import json
import pymysql
import datetime


timeout = 20
HOST = "39.97.241.144"
PORT = 3306
USER = "lianzhuoxinxi"
PASSWORD = 'LIANzhuoxinxi888?'
DATABASE = "spider"
CHARSET = "utf8"
start_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 开始时间

print("程序开始时间:{}".format(start_time))


class Proxies(object):
    """获取联卓信息企业代理(旗云代理网站)"""
    BASE_URL = "http://dev.110zy.cn/api/?apikey=45be735b785e8ed00752c4777e0dea8b1e200c2a" \
               "&num=30&type=json&line=mac&proxy_type=putong&sort=1&model=all&protocol=" \
               "http&address=%E5%8C%97%E4%BA%AC&kill_address=&port=&kill_port=&today=false&abroad=1" \
               "&isp=&anonymity=2"
    USERAGENT = UserAgent(verify_ssl=False).random

    def __init__(self):
        self.base_url = Proxies.BASE_URL
        self.user_agent = Proxies.USERAGENT
        self.response = None
        self.headers = {
            "User-Agent": self.user_agent
        }

    def proxies_get(self):
        if self.response is None:
            self.response = requests.get(self.base_url, headers=self.headers, verify=False, timeout=10).content

    def proxies_del(self):
        self.response = None
        self.proxies_get()

    def response_split(self):
        """response json to list to split to return"""
        self.response = json.loads(self.response.decode())

    def proxies_return(self):
        return self.response


def proxies():
    while True:
        try:
            P = Proxies()
            P.proxies_del()
            P.response_split()
            proxies_list = P.proxies_return()
        except json.decoder.JSONDecodeError:
            continue
        else:
            break
    return proxies_list


def user_agent():
    """获取UA"""
    u_a = UserAgent().random
    return u_a


def connect_mysql():
    # 链接mysql
    db = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        db=DATABASE,
        charset=CHARSET
    )
    return db


def insert_ranking_bill_board(source, bill_board_ranking_json):
    global start_time
    db = connect_mysql()
    update_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
    with db.cursor() as cursor:
        try:
            sql = "insert into spider.aso_app_store_list (`source`, `update_time`, " \
                  "`bill_board_ranking_json`, `start_time`) " \
                  "values ('{}', '{}', '{}', '{}')".format(source, update_time,
                                                           pymysql.escape_string(bill_board_ranking_json),start_time)
            cursor.execute(sql)
        except Exception as e:
            print(e)
        db.commit()
    db.close()


source_url_dict = {
    "总榜": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=36&popId=30",  # 总榜
    "儿童": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?ageBandId=0&cc=cn&genreId=36&pageOnly=true",  # 儿童
    "教育": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6017&popId=30&pageOnly=true",  # 教育
    "购物": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6024&popId=30&pageOnly=true",  # 购物
    "摄影与录像": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6008&popId=30&pageOnly=true",  # 摄影与录像
    "效率": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6007&popId=30&pageOnly=true",
    "美食佳饮": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6023&popId=30&pageOnly=true",
    "生活": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6012&popId=30&pageOnly=true",
    "健康健美": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6013&popId=30&pageOnly=true",
    "旅游": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6003&popId=30&pageOnly=true",
    "音乐": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6011&popId=30&pageOnly=true",
    "体育": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6004&popId=30&pageOnly=true",
    "商务": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6000&popId=30&pageOnly=true",
    "新闻": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6009&popId=30&pageOnly=true",
    "工具": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6002&popId=30&pageOnly=true",
    "娱乐": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6016&popId=30&pageOnly=true",
    "社交": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6005&popId=30&pageOnly=true",
    "报刊杂志": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6021&popId=30&pageOnly=true",
    "财务": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6015&popId=30&pageOnly=true",
    "参考": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6006&popId=30&pageOnly=true",
    "导航": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6010&popId=30&pageOnly=true",
    "医疗": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6020&popId=30&pageOnly=true",
    "图书": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6018&popId=30&pageOnly=true",
    "天气": "https://itunes.apple.com/WebObjects/MZStore.woa/wa/viewTop?cc=cn&genreId=6001&popId=30&pageOnly=true",
}


def json_write(path, info):
    with open(path, 'w') as f:
        f.write(info)
