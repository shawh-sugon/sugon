# * coding:utf-8 *
#.@FileName:test1
#.@Date:2020-05-02 : 09 : 39
"""
    本程序可实现nginx的自动安装，适用于liunx；且程序执行需要登录root用户
"""
#!/usr/bin/python
#coding=utf-8
import os
import sys

if os.getuid() == 0:
    cmd = "cd ~"
    res = os.system(cmd)
    if res != 0:
        print('进入用户目录失败')
        sys.exit(1)
else:
    print('当前用户不是root,请切换root用户执行')
    sys.exit(1)

#不是centos时 修改此处
cmd = "yum install gcc gcc-c++ automake pcre pcre-devel zlib zlib-devel openssl openssl-devel -y"
res = os.system(cmd)
if res != 0:
    print('缺少编译插件，请检查')
    sys.exit(1)

version = input('输入安装的nginx版本:\n1: 1.15版本；\n2: 1.14版本；\n3: 1.12版本；\n4: 1.10版本；\n5: 1.8版本；\n选择的版本是：')
if version == 1:
    url = 'http://nginx.org/download/nginx-1.15.8.tar.gz'
elif version == 2:
    url = 'http://nginx.org/download/nginx-1.14.2.tar.gz'
elif version == 3:
    url = 'http://nginx.org/download/nginx-1.12.2.tar.gz'
elif version == 4:
    url = 'http://nginx.org/download/nginx-1.10.3.tar.gz'
elif version == 5:
    url = 'http://nginx.org/download/nginx-1.8.1.tar.gz'
else:
    print('选择的版本号有误，请输入正确版本号')
    sys.exit(1)

cmd = 'wget ' + url
res = os.system(cmd)
if res != 0:
    print('下载源码包失败')
    sys.exit(1)

if version == 1:
    packpage_name = 'nginx-1.15.8'
elif version == 2:
    packpage_name = 'nginx-1.14.2'
elif version == 3:
    packpage_name = 'nginx-1.12.2'
elif version == 4:
    packpage_name = 'nginx-1.10.3'
else:
    packpage_name = 'nginx-1.8.1'
cmd = 'tar -zxvf ' + packpage_name+'.tar.gz'
res = os.system(cmd)
if res != 0:
    os.system('rm -rf '+packpage_name+'.tar.gz')
    print('下载失败，请重新运行')
    sys.exit(1)

cmd = 'cd ' +packpage_name+'&& ./configure --prefix=/usr/local/nginx && make && make install'
res = os.system(cmd)
if res != 0:
    print('编译失败')
    sys.exit(1)
else:
    print('编译安装完成')