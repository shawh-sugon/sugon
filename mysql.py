# * coding:utf-8 *
# .@FileName:mysql
# .@Date:2020-05-21 : 21 : 04
"""
    本程序可实现，mysql的自动安装，适用于liunx；且程序执行需要登录root用户
"""
# !/usr/bin/python
# coding=utf-8
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
cmd = "wget https://repo.mysql.com//mysql80-community-release-el7-3.noarch.rpm"
ret = os.system(cmd)
if ret != 0:
    print("下载失败！", cmd)
    sys.exit(1)

# 安装yum-utils防止安装报错
cmd = "yum -y install yum-utils"
ret = os.system(cmd)
if ret != 0:
    print("安装失败!", cmd)
    sys.exit(1)

# 安装mysql安装包
cmd = "yum localinstall mysql80-community-release-el7-3.noarch.rpm -y"
ret = os.system(cmd)
if ret != 0:
    print("安装失败!", cmd)
    sys.exit(1)
cmd = "yum-config-manager --enable mysql57-community"
cmd1 = "yum-config-manager --disable mysql80-community"
ret = os.system(cmd)
if ret != 0:
    print("安装失败！", cmd)
    sys.exit(1)
ret = os.system(cmd1)
if ret != 0:
    print("安装失败！", cmd1)
    sys.exit(1)

# 安装mysql关联包
cmd = "yum install mysql-community-server -y"
ret = os.system(cmd)
if ret != 0:
    print("安装失败！", cmd)
    sys.exit(1)

# 启动mysql程序,并设置开机启动
cmd = "systemctl start mysqld.service"
cmd1 = "systemctl enable mysqld.service"
ret = os.system(cmd)
if ret != 0:
    print("MySQL启动失败！", cmd)
    sys.exit(1)
ret = os.system(cmd1)
if ret != 0:
    print("设置MySQL开机自启动失败！", cmd1)
    sys.exit(1)

# 获取安装时的临时密码（在第一次登录时就是用这个密码）(知识点：find / -name mysql | xargs rm -rf；查找并删除)
cmd = "cat /var/log/mysqld.log | grep 'temporary password'"
ret = os.system(cmd)
if ret != 0:
    print("打开mysql密码文件失败！", cmd)
