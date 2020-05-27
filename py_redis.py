#!/usr/bin/env python
# encoding:utf-8
# -*- coding: utf-8 -*-

import os, sys

# 进入root用户的家目录
if os.getuid() == 0:
    cmd = "cd ~"
    ret = os.system(cmd)
    if ret != 0:
        print("进入家目录失败！", cmd)
        sys.exit(1)
else:
    print('当前用户不是root,请切换root用户执行')
    sys.exit(1)

# 下载安装包
cmd = "wget http://download.redis.io/releases/redis-4.0.6.tar.gz"
ret = os.system(cmd)
if ret != 0:
    print("下载失败！", cmd)
    sys.exit(1)
# 解压缩包
redis_path = "/usr/local/"
cmd = "tar -zxvf redis-4.0.6.tar.gz -C " + redis_path
ret = os.system(cmd)
if ret != 0:
    print("解压失败！", cmd)
    sys.exit(1)

# 安装gcc防止安装报错
cmd = "yum install gcc -y"
ret = os.system(cmd)
if ret != 0:
    print("安装失败!", cmd)
    sys.exit(1)

# 跳转路经并安装redis安装包
cmd = "cd " + redis_path + "redis-4.0.6 && make MALLOC=libc"
ret = os.system(cmd)
if ret != 0:
    print("跳转失败！")
    sys.exit(1)
else:
    print(cmd,"跳转成功！")

cmd = "cd " + redis_path + "redis-4.0.6/src && make install"
ret = os.system(cmd)
if ret != 0:
    print("安装失败！", cmd)
    sys.exit(1)

# 修改redis配置文件，设置成为后台启动
redis_conf = redis_path+"redis-4.0.6/redis.conf"
def alter(file,old_str,new_str):
    """
    将替换的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字
    :param file: 文件路径
    :param old_str: 需要替换的字符串
    :param new_str: 替换的字符串
    :return: None
    """
    with open(file, "r") as f1,open("%s.bak" % file, "w") as f2:
        for line in f1:
            if old_str in line:
                line = line.replace(old_str, new_str)
            f2.write(line)
    os.remove(file)
    os.rename("%s.bak" % file, file)

alter(redis_conf, "daemonize no", "daemonize yes")

# 设置开机自启动
cmd = "mkdir /etc/redis"
ret = os.system(cmd)
if ret != 0:
    print("创建失败！", cmd)
    sys.exit(1)
cmd = "cp /usr/local/redis-4.0.6/redis.conf /etc/redis/6379.conf && cp /usr/local/redis-4.0.6/utils/redis_init_script /etc/init.d/redisd"
ret = os.system(cmd)
if ret != 0:
    print("复制失败！", cmd)
    sys.exit(1)

redisd = "/etc/init.d/redisd"
list_a = ["# chkconfig:   2345 90 10","# description:  Redis is a persistent key-value database"]
def header_file(file_path,list_a):
    """
    向文件首行前添加内容
    :param file_path:所要修改文件的路径
    :param list_a: 添加的内容，列表类型
    :return:None
    """
    with open(file_path, "r") as f1, open("%s.bak" % file_path, "w") as f2:
        for i in f1.readlines():
            if i == "#!/bin/sh":
                list_a.insert(0, i)
            list_a.append(i)
        for i in list_a:
            f2.write(i)
    os.remove(file_path)
    os.rename("%s.bak" % file_path, file_path)
header_file(redisd,list_a)

cmd = "cd /etc/init.d && chkconfig redisd on"   # 这一步容易出现问题，
if ret != 0:
    print("设置失败！", cmd)
    sys.exit(1)

cmd = "service redisd start"
ret = os.system(cmd)
if ret != 0:
    print("Redis启动失败！", cmd)
    sys.exit(1)


# cmd = "cd " + redis_path + "redis-4.0.6/src && ./redis-server /usr/local/redis-4.0.6/redis.conf"
# ret = os.system(cmd)
# if ret != 0:
#     print("安装失败！", cmd)
#     sys.exit(1)