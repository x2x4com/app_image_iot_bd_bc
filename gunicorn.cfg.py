#!/usr/bin/env python
# encoding: utf-8
# ===============================================================================
#
#         FILE:
#
#        USAGE:
#
#  DESCRIPTION:
#
#      OPTIONS:  ---
# REQUIREMENTS:  ---
#         BUGS:  ---
#        NOTES:  ---
#       AUTHOR:  YOUR NAME (),
#      COMPANY:
#      VERSION:  1.0
#      CREATED:
#     REVISION:  ---
# ===============================================================================

# encoding: utf-8

import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing

bind = '0.0.0.0:8000'

preload_app = False

# 开启进程
# workers = 4
workers = multiprocessing.cpu_count() * 2

# 每个进程的开启线程
# threads = 1
threads = multiprocessing.cpu_count() * 16

backlog = 2048

# 工作模式为meinheld
# pip install meinheld
# worker_class = "egg:meinheld#gunicorn_worker"
worker_class = "gevent"

debug = True

# daemon = True

# 进程名称
proc_name = 'gunicorn.pid'

# 进程pid记录文件
pidfile = '/tmp/gunicorn.pid'

loglevel = 'info'
logfile = '/tmp/gunicorn.log'

# 设置gunicorn访问日志格式，错误日志无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

"""
其每个选项的含义如下：
h          remote address
l          '-'
u          currently '-', may be user name in future releases
t          date of the request
r          status line (e.g. ``GET / HTTP/1.1``)
s          status
b          response length or '-'
f          referer
a          user agent
T          request time in seconds
D          request time in microseconds
L          request time in decimal seconds
p          process ID
"""
# 访问日志文件
accesslog = "-"

errorlog = "-"


