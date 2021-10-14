# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/18 9:59 
# @Author : lijun7 
# @File : ping_ip.py
# @desc : cdn迁移ping ip地址
"""
import os
import re


def ping_ips(host_path, ip_path):
    if os.path.exists(ip_path):
        os.remove(ip_path)
    with open(host_path, 'r', encoding='utf8') as file_read:
        for hosts in file_read.readlines():
            if hosts == '\n':
                break
            host = hosts.split(',')
            result = os.popen('ping -w 1000 -n 1 %s' % host[0]).read()
            if 'TTL' in result:
                ip = re.search('\\[(.*?)\\]', result).group(1)
            print('%s %s %s' % (ip, host[0], host[1]))
            with open(ip_path, 'a') as file_write:
                file_write.write('%s %s\n' % (ip.strip(), host[1].strip()))


def ping_ip(host):
    result = os.popen('ping -w 1000 -n 1 %s' % host).read()
    print(result)


if __name__ == '__main__':
    host_dict = {
        'user.zaful.com': 'd32oojk6oy7xcs.cloudfront.net',
        'www.zaful.com': 'd2p45setawhpc.cloudfront.net'
    }

    cloudfront = host_dict.get('user.zaful.com')
    ping_ip('cashier.gearbest.com')
    # 所有站点
    # ping_ips(host_path='./resource/zf_hosts.txt', ip_path='./resource/zf_ip.txt')
    # 支付、支持中心
    # ping_ips(host_path='./resource/hosts.txt',ip_path='./resource/pay_ip.txt')
