# coding=UTF-8
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA

cleaned = '/home/lt/data/tianchi/cleaned/'
# 2014.04.01~2014.07.31
offline_train = cleaned + 'offline/train/'
# 2014.08.31~2014.08.31
offline_test = cleaned + 'offline/test/'
# 2014.05.01~2014.08.31
online_train = cleaned + 'online/train/'
# 2014.09.01~2014.09.30
online_test = cleaned + 'online/test/'

def gen_y_by_day(data):
    grouped = data.groupby('report_date')
    purchase = grouped['total_purchase_amt'].sum()
    purchase.to_csv('/home/lt/data/tianchi/purchase_by_day.csv')
    redeem = grouped['total_redeem_amt'].sum()
    redeem.to_csv('/home/lt/data/tianchi/redeem_by_day.csv')
    
# def gen_share_by_day(data):
#     dates = pd.date_range('20130701', '20140831', 'D')
#     i = 0
#     for i in range(data.size):
#         if data['mfd_date'] != dates[i]:
#             data.append(data.idx)

def gen_online_offline_X():
    # 2013.07.01~2014.08.31
    purchase_features = pd.read_csv(cleaned+'purchase_features.csv', header=0, parse_dates='report_date', index_col='report_date')
    redeem_features = pd.read_csv(cleaned+'redeem_features.csv', header=0, parse_dates='report_date', index_col='report_date')
    # 2014.09.01~2014.09.30
    sep_purchase_features = pd.read_csv(cleaned+'sep_purchase_features.csv', header=0, parse_dates='report_date', index_col='report_date')
    sep_redeem_features = pd.read_csv(cleaned+'sep_redeem_features.csv', header=0, parse_dates='report_date', index_col='report_date')
    
    # generate data
    offline_train_X_purchase = purchase_features.ix[pd.date_range('20140401', '20140731',freq='D')]
    offline_train_X_redeem = redeem_features.ix[pd.date_range('20140401', '20140731',freq='D')]
    offline_test_X_purchase = purchase_features.ix[pd.date_range('20140801', '20140831',freq='D')]
    offline_test_X_redeem = redeem_features.ix[pd.date_range('20140801', '20140831',freq='D')]
    online_train_X_purchase = purchase_features.ix[pd.date_range('20140501', '20140831',freq='D')]
    online_train_X_redeem = redeem_features.ix[pd.date_range('20140501', '20140831',freq='D')]
    online_test_X_purchase = sep_purchase_features
    online_test_X_redeem = sep_redeem_features
    
    # output data
    offline_train_X_purchase.to_csv(offline_train+'X_purchase.csv', index_label='report_date')
    offline_train_X_redeem.to_csv(offline_train+'X_redeem.csv', index_label='report_date')
    offline_test_X_purchase.to_csv(offline_test+'X_purchase.csv', index_label='report_date')
    offline_test_X_redeem.to_csv(offline_test+'X_redeem.csv', index_label='report_date')
    online_train_X_purchase.to_csv(online_train+'X_purchase.csv', index_label='report_date')
    online_train_X_redeem.to_csv(online_train+'X_redeem.csv', index_label='report_date')
    online_test_X_purchase.to_csv(online_test+'X_redeem.csv', index_label='report_date')
    online_test_X_redeem.to_csv(online_test+'X_redeem.csv', index_label='report_date')
    
if __name__ == '__main__':
    gen_online_offline_X()
    