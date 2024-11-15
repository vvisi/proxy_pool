# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

import re
import json
from time import sleep

from util.webRequest import WebRequest


class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        站大爷 【实时更新】https://www.zdaye.com/free/1/
        """        
        nums = 5
        for i in range(1, int(nums)+1):
            target_url = "https://www.zdaye.com/free/"+str(i)+"/"
            _tree = WebRequest().get(target_url).tree
            for tr in _tree.xpath("//table//tr"):
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                yield "%s:%s" % (ip, port) 
            sleep(5)


    @staticmethod
    def freeProxy02():
        """
        代理66 http://www.66ip.cn/
        """
        url = "http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=http%3A%2F%2Fwww.66ip.cn%2F%3Fsxb%3D%26tqsl%3D100%26ports%255B%255D2%3D%26ktip%3D%26sxa%3D%26radio%3Dradio%26submit%3D%25CC%25E1%2B%2B%25C8%25A1"
        r = WebRequest().get(url, timeout=10)
        proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)', r.text)
        yield from proxies

    @staticmethod
    def freeProxy03():
        """ 开心代理 """
        urls = ["http://www.kxdaili.com/dailiip.html", "http://www.kxdaili.com/dailiip/2/1.html"]
        for url in urls:
            r = WebRequest().get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            yield from [':'.join(proxy) for proxy in proxies]

            more_urls = re.findall(r'<a\s+href=\"(/dailiip/\d+/\d+.html)\">\d+</a>', r.text)
            more_urls = [urllib.parse.urljoin(url, more_url) for more_url in more_urls]
            for more_url in more_urls:
                sleep(1)
                r = WebRequest().get(more_url)
                proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
                yield from [':'.join(proxy) for proxy in proxies]

    @staticmethod
    def freeProxy04():
        """ lumiproxy"""
        url = "https://api.lumiproxy.com/web_v1/free-proxy/list?page_size=60&page=1&language=zh-hans"
        r = WebRequest().get(url)
        #print(type(r.text))
        jsonstr = json.loads(r.text)
        #print(type(jsonstr))
        try:
            for each in jsonstr['data']['list']:
                yield "%s:%s" % (each['ip'], each['port'])
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy05(page_count=1):
        """ 快代理 https://www.kuaidaili.com """
        url_pattern = [
            'https://www.kuaidaili.com/free/dps/{}/',
            'https://www.kuaidaili.com/free/fps/{}/'
        ]
        url_list = []
        for page_index in range(1, page_count+1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            response = WebRequest().get(url)
            #print(response.text)
            # 使用正则表达式提取JSON数组  
            json_pattern = r'const fpsList = (\[.*?\]);'  
            match = re.search(json_pattern, response.text)  
            if match: 
                json_data_str = match.group(1)  
                #print(json_data_str)
                # 解析JSON数据  
                json_data = json.loads(json_data_str)  
                
                # 提取IP地址和端口号  
                for item in json_data:  
                    ip = item.get('ip')  
                    port = item.get('port')  
                    yield "%s:%s" % (ip, port) 
            else:  
                print("未找到匹配的JSON数据")

    @staticmethod
    def freeProxy06():
        """ 云代理 """
        urls = ['http://www.ip3366.net/free/?stype=1', "http://www.ip3366.net/free/?stype=2"]
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)

    @staticmethod
    def freeProxy07():
        """ 小幻代理 """
        now = datetime.now()
        url = f'https://ip.ihuan.me/today/{now.year}/{now.month:02}/{now.day:02}/{now.hour:02}.html'
        r = WebRequest().get(url, timeout=10)
        proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)', r.text)
        yield from [':'.join(proxy) for proxy in proxies]

    @staticmethod
    def freeProxy8():
        """ 89免费代理 5"""
        urls = ['https://www.89ip.cn/']
        while True:
            try:
                url = urls.pop()
            except IndexError:
                break

            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                r.text)
            if not proxies:
                # 没了
                break

            yield from [':'.join(proxy) for proxy in proxies]

            # 下一页
            r = re.findall(r'<a\s+href=\"(index_\d+.html)\"\s+class=\"layui-laypage-next\"\s+data-page=\"\d+\">下一页</a>', r.text)
            if r:
                next_url = urllib.parse.urljoin(url, r[0])
                urls.append(next_url)
                sleep(1)

    @staticmethod
    def freeProxy9():
        """ 稻壳代理 https://www.docip.net/ """
        r = WebRequest().get("https://www.docip.net/data/free.json", timeout=10)
        try:
            for each in r.json['data']:
                yield each['ip']
        except Exception as e:
            print(e)
    @staticmethod
    def freeProxy10():
        url = 'https://gh-proxy.com/https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.json'
        r = WebRequest().get(url, timeout=10)
        proxies = [f'{proxy["ip"]}:{proxy["port"]}' for proxy in  r.json]
        yield from proxies

    @staticmethod
    def freeProxy11():
        url = 'https://gh-proxy.com/https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt'
        r = WebRequest().get(url, timeout=10)
        proxies = [proxy for proxy in r.text.split('\n') if proxy]
        yield from proxies

    @staticmethod
    def freeProxy12():
        url = 'https://sunny9577.github.io/proxy-scraper/proxies.json'
        r = WebRequest().get(url, timeout=10)
        proxies = [f'{proxy["ip"]}:{proxy["port"]}' for proxy in  r.json]
        yield from proxies

    @staticmethod
    def freeProxy13():
        urls = ['https://gh-proxy.com/https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt', 'https://gh-proxy.com/https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt']
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = [':'.join(proxy.split(':')[:2]) for proxy in r.text.split('\n') if proxy]
            yield from proxies

    @staticmethod
    def freeProxy14():
        url = 'https://iproyal.com/free-proxy-list/?page=1&entries=100'

        while True:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</div><div class=\"flex items-center astro-lmapxigl\">(\d+)</div>', r.text)
            yield from [':'.join(proxy) for proxy in proxies]

            next = r.tree.xpath('//a[text()="Next"]/@href')
            if next:
                url = urllib.parse.urljoin(url, next[0])
                sleep(5)
            else:
                break

    @staticmethod
    def freeProxy15():
        urls = ['http://pubproxy.com/api/proxy?limit=5&https=true', 'http://pubproxy.com/api/proxy?limit=5&https=false']
        proxies = set()
        for url in urls:
            for _ in range(10):
                sleep(1)
                r = WebRequest().get(url, timeout=10)
                for proxy in [proxy['ipPort'] for proxy in r.json['data']]:
                    if proxy in proxies:
                        continue
                    yield proxy
                    proxies.add(proxy)

    @staticmethod
    def freeProxy16():
        urls = ['https://freeproxylist.cc/servers/']
        while True:
            try:
                url = urls.pop()
            except IndexError:
                break

            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            yield from [':'.join(proxy) for proxy in proxies]

            r = re.findall(r'''<a\s+href='(https://freeproxylist\.cc/servers/\d+\.html)'>&raquo;</a></li>''', r.text)
            if r:
                urls.append(r[0])
                sleep(1)

    @staticmethod
    def freeProxy17():
        url = 'https://hasdata.com/free-proxy-list'
        r = WebRequest().get(url, timeout=10)
        proxies = re.findall(r'<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d+)</td><td>HTTP', r.text)
        yield from [':'.join(proxy) for proxy in proxies]

    @staticmethod
    def freeProxy18():
        urls = ['https://www.freeproxy.world/?type=https&anonymity=&country=&speed=&port=&page=1', 'https://www.freeproxy.world/?type=http&anonymity=&country=&speed=&port=&page=1']
        for url in urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*</td>\s*<td>\s*<a href=\"/\?port=\d+\">(\d+)</a>', r.text)
            yield from [':'.join(proxy) for proxy in proxies]


if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy01():
        print(_)
