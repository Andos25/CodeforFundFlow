#!/usr/bin/env python
#-*- encoding:utf-8 -*-
__author__ = 'kangkona'

from pyspark import SparkContext, SparkConf
from datetime import time, datetime

def line2Balance(line):
    tmps = line.split(',')
    items = []
    for tmp in tmps:
        if tmp == '':
            tmp = '0'
        items.append(tmp)
    report_date = items[1][:4] + '-' + items[1][4:6] + '-' + items[1][6:]
    moneys = tuple([int(item) for item in items[2:]])
    return (report_date, moneys)

def sumBalance(dailyBalance):
    return (dailyBalance[0], reduce(lambda b1, b2 : tuple([b1[i] + b2[i] for i in range(len(b1))]), \
                                    dailyBalance[1]))

def dailyBalanceCount(dstFile):
    conf = (SparkConf()
            .setMaster("local")
            .setAppName("daily_durations_count")
            .set("spark.executor.memory", "10g"))
    sc = SparkContext(conf = conf)
    lines = sc.textFile("hdfs:///user/hanyunfei/cashio/data/user_balance_table.csv")
    lines.map(lambda line : line2Balance(line)) \
        .groupByKey(16) \
        .map(sumBalance) \
        .map(lambda x : ','.join([x[0]] + [str(item) for item in x[1]])) \
        .saveAsTextFile(dstFile)

if __name__ == '__main__':
    dailyBalanceCount("hdfs:///user/hanyunfei/cashio/result/daily_balance_count.csv")