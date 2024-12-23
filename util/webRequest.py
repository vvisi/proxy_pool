# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     WebRequest
   Description :   Network Requests Class
   Author :        J_hao
   date：          2017/7/31
-------------------------------------------------
   Change Activity:
                   2017/7/31:
-------------------------------------------------
"""
__author__ = 'J_hao'

import random
import time

import requests
from handler.logHandler import LogHandler
from lxml import etree
from requests.models import Response

requests.packages.urllib3.disable_warnings()


class WebRequest(object):
    name = "web_request"

    def __init__(self, *args, **kwargs):
        self.log = LogHandler(self.name, file=False)
        self.response = Response()

    @property
    def user_agent(self):
        """
        return an User-Agent at random
        :return:
        """
        ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0',
        ]
        return random.choice(ua_list)

    @property
    def header(self):
        """
        basic header
        :return:
        """
        return {
            'User-Agent': self.user_agent,
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }

    def get(
        self,
        url,
        header=None,
        retry_time=3,
        retry_interval=5,
        timeout=5,
        *args,
        **kwargs
    ):
        """
        get method
        :param url: target url
        :param header: headers
        :param retry_time: retry time
        :param retry_interval: retry interval
        :param timeout: network timeout
        :return:
        """
        headers = self.header
        if header and isinstance(header, dict):
            headers.update(header)
        while True:
            try:
                self.response = requests.get(
                    url, headers=headers, timeout=timeout, *args, **kwargs
                )
                return self
            except Exception as e:
                self.log.error("requests: %s error: %s" % (url, str(e)))
                retry_time -= 1
                if retry_time <= 0:
                    resp = Response()
                    resp.status_code = 200
                    return self
                self.log.info("retry %s second after" % retry_interval)
                time.sleep(retry_interval)

    @property
    def tree(self):
        return etree.HTML(self.response.content)

    @property
    def text(self):
        return self.response.text

    @property
    def json(self):
        try:
            return self.response.json()
        except Exception as e:
            self.log.error(str(e))
            return {}
