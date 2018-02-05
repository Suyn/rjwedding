# -*- coding:utf-8 -*-
import time


def beijing_time(self):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+46800))
