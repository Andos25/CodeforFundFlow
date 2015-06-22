#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'kangkona'

'''
#####################
加入7个特征: 过去一周 每天的 phrchase - redeem
sum of squared relative errors:  1.05894715005
mean of absolute errors:  0.149488305549
std of errors:  0.158459638824

#####################
next step:  在计算净流入的情况下考虑利率波动
净流入 = (流入 - 收益) - (流出 - 购物)
'''
#      n_estimators,max_depth,learning_rate
'''
115: purchase:{639,1,0.01}       redeem{665,3,0.02},  特征是new文件夹下的特征
'''


'''
2015-06-22: purchase:{523,1,0.01}  redeem{998,1,0.02}, 加入的特征为relativedays, (report_date - 20130701)/7
'''