#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2024/4/14 下午7:47
# file: 1.双色球爬虫.py
# author: TonyEinstein
# email: 116338825+TonyEinstein@users.noreply.github.com








# https://www.zhcw.com/kjxx/ssq/kjxq/?kjData=2005009


if __name__ == '__main__':
    # 开奖年
    year = [i for i in range(2003,2015)]
    # 期数
    period = [f"{i:03}" for i in range(1, 151)]
    print(period)