# -*- coding=utf-8 -*-
# @Time : 2019/6/26 9:41 
# @Author : piller
# @File : ranking_bill_board_spider.py
# @Software: PyCharm
import sys
from os.path import abspath, join, dirname
import requests
import random
import json
import time
sys.path.insert(0, join(abspath(dirname(__file__)), '../'))
from settings import proxies, user_agent, source_url_dict, timeout, insert_ranking_bill_board, json_write


def headers():
    # 配置请求头
    header = {
        "User-Agent": "{}".format(user_agent()),
        "x-apple-store-front": "143465-19,29"
    }
    return header


def proxy():
    # 配置代理
    proxies_list = proxies()
    ip_port = random.choice(proxies_list)
    agent = {
        "http": ip_port
    }
    print("目前使用代理为:{}".format(agent))
    return agent


def get_source_url():
    for key, value in source_url_dict.items():
        yield (key, value)


def su_next(su):
    try:
        key, value = su.__next__()
        return key, value
    except StopIteration:
        pass


def main():
    """流程调转"""
    error_number = 0
    su = get_source_url()
    while 1:
        # 1.为requests配置UA, 请求参数, proxies, 请求时间 {headers(), proxies()}
        # 2.请求榜单页,
        key, value = su_next(su)
        while 1:
            try:
                pass
                response = requests.get(value, headers=headers(), proxies=proxy(), timeout=timeout)
                print("本次请求为{}页, 该页状态码为{}".format(key, response.status_code))
                # 3.整个文件存入数据库
                bill_board_ranking_json = response.content.decode()
                print(type(bill_board_ranking_json))
                # base_path = "/home/gogs/spider/billBoardInfo/"
                base_path = "./"

                path = base_path + str(int(time.time() * 1000)) + ".json"
                json_write(path, bill_board_ranking_json)
                insert_ranking_bill_board(source=key, bill_board_ranking_json=path)
            except requests.exceptions.ConnectTimeout:
                error_number += 1
                print("请求失败, 当前第{}次请求".format(error_number))
                if error_number >= 10:
                    error_number = 0
                    break
                continue
            except requests.exceptions.ConnectionError:
                error_number += 1
                print("请求失败, 当前第{}次请求".format(error_number))
                if error_number >= 10:
                    error_number = 0
                    break
                continue
            except requests.exceptions.Timeout:
                error_number += 1
                print("请求失败, 当前第{}次请求".format(error_number))
                if error_number >= 10:
                    error_number = 0
                    break
                continue
            else:
                error_number = 0
                break


if __name__ == '__main__':
    main()
