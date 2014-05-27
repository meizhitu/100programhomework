#coding=utf-8
import socket
import urllib2
import json


def getIpInfo(ipaddress):
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ipaddress
    page = urllib2.urlopen(url)
    data = page.read()
    jsondata = json.loads(data)
    if jsondata[u'code'] == 0:
        print '所在国家：' + jsondata[u'data'][u'country'].encode('utf-8')
        print '所在地区：' + jsondata[u'data'][u'area'].encode('utf-8')
        print '所在省份：' + jsondata[u'data'][u'region'].encode('utf-8')
        print '所在城市：' + jsondata[u'data'][u'city'].encode('utf-8')
        print '所用运营商：' + jsondata[u'data'][u'isp'].encode('utf-8')
    else:
        print '查询失败 请检查IP 后再说'


if __name__ == "__main__":
    ip = socket.gethostbyname('baidu.com')
    print(ip)
    getIpInfo(ip)
    ip = socket.gethostbyname(socket.gethostname())
    print(ip)
    getIpInfo(ip)
    localname = socket.getfqdn(socket.gethostname())
    ip = socket.gethostbyname(localname)
    print(ip)
    getIpInfo(ip)
    print('-' * 10)
    ipList = socket.gethostbyname_ex(socket.gethostname())
    for i in ipList:
        print(i)
