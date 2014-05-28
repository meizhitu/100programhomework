#coding=utf-8
import socket
import urllib2
import json
import sys

PY2 = sys.version_info.major == 2
import functools
import os
import struct

_unpack_V = lambda b: struct.unpack("<L", b)
_unpack_N = lambda b: struct.unpack(">L", b)
_unpack_C = lambda b: struct.unpack("B", b)

with open(os.path.join(os.path.dirname(__file__), "17monipdb.dat"), "rb") as f:
    dat = f.read()
    offset, = _unpack_N(dat[:4])
    index = dat[4:offset]


def memoize(func):
    """Memoize for functions based on memory
    """
    cache = func.cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = "{0}{1}".format(args, kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


@memoize
def _find_ip(ip):
    nip = socket.inet_aton(ip)

    tmp_offset = int(ip.split(".")[0]) * 4
    start, = _unpack_V(index[tmp_offset:tmp_offset + 4])

    index_offset = index_length = 0
    max_comp_len = offset - 1028
    start = start * 8 + 1024
    while start < max_comp_len:
        if index[start:start + 4] >= nip:
            index_offset, = _unpack_V(
                index[start + 4:start + 7] + chr(0).encode("utf-8"))
            if PY2:
                index_length, = _unpack_C(index[start + 7])
            else:
                index_length = index[start + 7]
            break
        start += 8

    if index_offset == 0:
        return
    res_offset = offset + index_offset - 1024
    return dat[res_offset:res_offset + index_length].decode("utf-8")


def find(ip):
    try:
        ip = socket.gethostbyname(ip)
    except socket.gaierror:
        return
    return _find_ip(ip)


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
    print(u"离线：" + find(ip))
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
