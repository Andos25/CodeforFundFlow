# coding=UTF-8
import pandas as pd
from sklearn import ensemble
from sklearn.metrics import mean_squared_error
from predict_models.metrics import data_compare, error_plot, get_metrics, residual_analysis
import numpy as np
import matplotlib.pyplot as plt

online = '/home/lt/data/tianchi/cleaned/online/'
offline = '/home/lt/data/tianchi/cleaned/offline/'

online_train_X_purchase = pd.read_csv(online+'train/X_purchase.csv', header=0, parse_dates='report_date', index_col='report_date')
online_train_X_redeem = pd.read_csv(online+'train/X_redeem.csv', header=0, parse_dates='report_date', index_col='report_date')
online_train_y_purchase = pd.read_csv(online+'train/y_purchase.csv', header=0, parse_dates='report_date', index_col='report_date')['total_purchase_amt']
online_train_y_redeem = pd.read_csv(online+'train/y_redeem.csv', header=0, parse_dates='report_date', index_col='report_date')['total_redeem_amt']
online_test_X_purchase = pd.read_csv(online+'test/X_purchase.csv', header=0, parse_dates='report_date', index_col='report_date')
online_test_X_redeem = pd.read_csv(online+'test/X_redeem.csv', header=0, parse_dates='report_date', index_col='report_date')

offline_train_X_purchase = pd.read_csv(offline+'train/X_purchase.csv', header=0, parse_dates='report_date', index_col='report_date')
offline_train_X_redeem = pd.read_csv(offline+'train/X_redeem.csv', header=0, parse_dates='report_date', index_col='report_date')
offline_train_y_purchase = pd.read_csv(offline+'train/y_purchase.csv', header=0, parse_dates='report_date', index_col='report_date')['total_purchase_amt']
offline_train_y_redeem = pd.read_csv(offline+'train/y_redeem.csv', header=0, parse_dates='report_date', index_col='report_date')['total_redeem_amt']
offline_test_X_purchase = pd.read_csv(offline+'test/X_purchase.csv', header=0, parse_dates='report_date', index_col='report_date')
offline_test_X_redeem = pd.read_csv(offline+'test/X_redeem.csv', header=0, parse_dates='report_date', index_col='report_date')
offline_test_y_purchase = pd.read_csv(offline+'test/y_purchase.csv', header=0, parse_dates='report_date', index_col='report_date')['total_purchase_amt']
offline_test_y_redeem = pd.read_csv(offline+'test/y_redeem.csv', header=0, parse_dates='report_date', index_col='report_date')['total_redeem_amt']

purchase_params = {'n_estimators':87, 'max_depth':3, 'random_state':0, 'min_samples_split':4,
              'learning_rate':0.34, 'loss':'lad'}
redeem_params = {'n_estimators':60, 'max_depth':2, 'random_state':0, 'min_samples_split':4,
              'learning_rate':0.48, 'loss':'lad'}

def online_predict():
    purchase_clf = ensemble.GradientBoostingRegressor(**purchase_params).fit(online_train_X_purchase, online_train_y_purchase)
    redeem_clf = ensemble.GradientBoostingRegressor(**redeem_params).fit(online_train_X_redeem, online_train_y_redeem)
    sep = pd.date_range('20140901', '20140930', freq='D')
    sep_purchase = pd.DataFrame(index=sep)
    sep_redeem = pd.DataFrame(index=sep)
    for date in sep:
        print online_test_X_purchase.ix[date]
        today_pur = purchase_clf.predict(online_test_X_purchase.ix[date])
        today_red = redeem_clf.predict(online_test_X_redeem.ix[date])
        sep_purchase.ix[date, 'total_purchase_amt'] = today_pur
        sep_redeem.ix[date, 'total_redeem_amt'] = today_red
        
        nextday = date + 1
        # yesterday
        online_test_X_purchase.ix[nextday, 'yesterday_purchase'] = today_pur
#         online_test_X_purchase.ix[nextday,'yesterday_redeem'] = today_red
#         online_test_X_redeem.ix[nextday,'yesterday_purchase'] = today_pur
        online_test_X_redeem.ix[nextday,'yesterday_redeem'] = today_red
##############################################################################################################################
#         # purchase week
#         weeknums1 = [nextday-7, nextday -14, nextday -21, nextday -28]
#         col_names1 = ['week1_purchase', 'week2_purchase', 'week3_purchase', 'week4_purchase']
#         for i in range(len(weeknums1)):
#             weeknum = weeknums1[i]
#             col_name = col_names1[i]
#             if weeknum in sep:
#                 online_test_X_purchase.ix[nextday,col_name] = sep_purchase.ix[weeknum, 'total_purchase_amt']
#             else:
#                 online_test_X_purchase.ix[nextday,col_name] = online_train_y_purchase.ix[weeknum, 'total_purchase_amt']
#         # redeem week        
#         col_names2 = ['week1_redeem', 'week2_redeem', 'week3_redeem', 'week4_redeem']
#         for i in range(len(weeknums1)):
#             weeknum = weeknums1[i]
#             col_name = col_names2[i]
#             if weeknum in sep:
#                 online_test_X_redeem.ix[nextday,col_name] = sep_redeem.ix[weeknum, 'total_redeem_amt']
#             else:
#                 online_test_X_redeem.ix[nextday,col_name] = online_train_y_redeem.ix[weeknum, 'total_redeem_amt']
#   
#         weeknums2 = [nextday-7, nextday -14, nextday -21]
#         # purchase redeem week
#         col_names3 = ['week1_redeem', 'week2_redeem', 'week3_redeem']
#         for i in range(len(weeknums2)):
#             weeknum = weeknums2[i]
#             col_name = col_names3[i]
#             if weeknum in sep:
#                 online_test_X_purchase.ix[nextday,col_name] = sep_redeem.ix[weeknum, 'total_redeem_amt']
#             else:
#                 online_test_X_purchase.ix[nextday,col_name] = online_train_y_redeem.ix[weeknum, 'total_redeem_amt']
#         # redeem purchase week
#         col_names4 = ['week1_purchase', 'week2_purchase', 'week3_purchase']
#         for i in range(len(weeknums2)):
#             weeknum = weeknums2[i]
#             col_name = col_names4[i]
#             if weeknum in sep:
#                 online_test_X_redeem.ix[nextday,col_name] = sep_purchase.ix[weeknum, 'total_purchase_amt']
#             else:
#                 online_test_X_redeem.ix[nextday,col_name] = online_train_y_purchase.ix[weeknum, 'total_purchase_amt']
#################################################################################################################################
#         weeks
        do_week(nextday -7, sep, nextday, sep_purchase, sep_redeem, 'week1')
        do_week(nextday -14, sep, nextday, sep_purchase, sep_redeem, 'week2')
        do_week(nextday -21, sep, nextday, sep_purchase, sep_redeem, 'week3')
        do_week(nextday -28, sep, nextday, sep_purchase, sep_redeem, 'week4')
        
    sep_purchase.to_csv('/home/lt/data/tianchi/tmp_pur.csv')
    sep_redeem.to_csv('/home/lt/data/tianchi/tmp_red.csv')

def do_week(weeknum, sep, nextday, sep_purchase, sep_redeem, col_name1):
    if weeknum in sep:
        online_test_X_purchase.ix[nextday,col_name1+'_purchase'] = sep_purchase.ix[weeknum, 'total_purchase_amt']
        online_test_X_redeem.ix[nextday,col_name1+'_redeem'] = sep_redeem.ix[weeknum, 'total_redeem_amt']
    else:
        online_test_X_purchase.ix[nextday,col_name1+'_purchase'] = online_train_y_purchase.ix[weeknum, 'total_purchase_amt']
        online_test_X_redeem.ix[nextday,col_name1+'_redeem'] = online_train_y_redeem.ix[weeknum, 'total_redeem_amt']
        
def offline_predict(predict_type, X_train, y_train, X_test):
    params = {}
    if predict_type == 'purchase':
        params = purchase_params
    elif predict_type == 'redeem':
        params = redeem_params
    # 20140401~20140831
    clf = ensemble.GradientBoostingRegressor(**params)
    clf.fit(X_train, y_train)
    offline_predict = clf.predict(X_test)
    return offline_predict

def select_params(train_type, param_type, candidates):
    param = []
    mean_errors = []
    if train_type == 'purchase':
        for candicate in candidates:
            purchase_params[param_type] = candicate
            offline_predict_purchase = offline_predict('purchase', offline_train_X_purchase, offline_train_y_purchase, offline_test_X_purchase)
            [sum_error,mean_error,std_error] = get_metrics(offline_test_y_purchase, offline_predict_purchase)
            param.append(candicate)
            mean_errors.append(mean_error)
        plt.scatter(param, mean_errors)
        plt.show()
    elif train_type == 'redeem':
        for candicate in candidates:
            redeem_params[param_type] = candicate
            offline_predict_redeem = offline_predict('redeem', offline_train_X_redeem, offline_train_y_redeem, offline_test_X_redeem)
            [sum_error,mean_error,std_error] = get_metrics(offline_test_y_redeem, offline_predict_redeem)
            param.append(candicate)
            mean_errors.append(mean_error)
        plt.scatter(param, mean_errors)
        plt.show()
    print param[mean_errors.index(min(mean_errors))], min(mean_errors)
    
if __name__ == '__main__':
    # online
#     online_predict()

#     # offline
    offline_predict_purchase = offline_predict('purchase', offline_train_X_purchase, offline_train_y_purchase, offline_test_X_purchase)
    error_plot(offline_test_y_purchase, offline_predict_purchase, "")
    residual_analysis(offline_test_y_purchase, offline_predict_purchase)
# 
#     offline_predict_redeem = offline_predict('redeem', offline_train_X_redeem, offline_train_y_redeem, offline_test_X_redeem)
#     error_plot(offline_test_y_redeem, offline_predict_redeem, "")

#     select_params('purchase', 'n_estimators', np.arange(20, 400, 1))
#     select_params('purchase', 'learning_rate', np.arange(0.01, 0.50, 0.01))

#     select_params('redeem', 'n_estimators', np.arange(20, 400, 1))
#     select_params('redeem', 'learning_rate', np.arange(0.01, 0.50, 0.01))
    