# coding=UTF-8
import pandas as pd
from sklearn import ensemble
from sklearn.metrics import mean_squared_error
from predict_models.metrics import data_compare, error_plot

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

purchase_params = {'n_estimators':108, 'max_depth':3, 'random_state':0, 'min_samples_split':4,
              'learning_rate':0.07, 'loss':'lad'}
redeem_params = {'n_estimators':2800, 'max_depth':2, 'random_state':0, 'min_samples_split':4,
              'learning_rate':0.01, 'loss':'lad'}

def online_predict():
    purchase_clf = ensemble.GradientBoostingRegressor(**purchase_params).fit(online_train_X_purchase, online_train_y_purchase)
    redeem_clf = ensemble.GradientBoostingRegressor(**redeem_params).fit(online_train_X_redeem, online_train_y_redeem)
    sep = pd.date_range('20140901', '20140930', freq='D')
    sep_purchase = pd.DataFrame(index=sep)
    sep_redeem = pd.DataFrame(index=sep)
    for date in sep:
        print date
        today_pur = purchase_clf.predict(online_test_X_purchase.ix[date])
        today_red = redeem_clf.predict(online_test_X_redeem.ix[date])
        sep_purchase.ix[date, 'total_purchase_amt'] = today_pur
        sep_redeem.ix[date, 'total_redeem_amt'] = today_red
        
        nextday = date + 1
        # yesterday
        online_test_X_purchase.ix[nextday, 'yesterday_purchase'] = today_pur
        online_test_X_purchase.ix[nextday,'yesterday_redeem'] = today_red
        online_test_X_redeem.ix[nextday,'yesterday_purchase'] = today_pur
        online_test_X_redeem.ix[nextday,'yesterday_redeem'] = today_red
        
        # weeks
        do_week(nextday -7, sep, nextday, sep_purchase, sep_redeem, 'week1')
        do_week(nextday -14, sep, nextday, sep_purchase, sep_redeem, 'week2')
        do_week(nextday -21, sep, nextday, sep_purchase, sep_redeem, 'week3')
        do_week(nextday -28, sep, nextday, sep_purchase, sep_redeem, 'week4')
        
#         print online_test_X_purchase.ix[nextday], online_test_X_redeem.ix[nextday]
    sep_purchase.to_csv('/home/lt/data/tianchi/tmp_pur.csv')
    sep_redeem.to_csv('/home/lt/data/tianchi/tmp_red.csv')

def do_week(weeknum, sep, nextday, sep_purchase, sep_redeem, col_name):
    if weeknum in sep:
        online_test_X_purchase.ix[nextday,col_name] = sep_purchase.ix[weeknum, 'total_purchase_amt']
        online_test_X_redeem.ix[nextday,col_name] = sep_redeem.ix[weeknum, 'total_redeem_amt']
    else:
        online_test_X_purchase.ix[nextday,col_name] = online_train_y_purchase.ix[weeknum, 'total_purchase_amt']
        online_test_X_redeem.ix[nextday,col_name] = online_train_y_redeem.ix[weeknum, 'total_redeem_amt']
        
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

if __name__ == '__main__':
    # online
#     online_predict()

    # offline
#     offline_predict_purchase = offline_predict('purchase', offline_train_X_purchase, offline_train_y_purchase, offline_test_X_purchase)
# #     data_compare(offline_test_y_purchase, offline_predict_purchase)
#     error_plot(offline_test_y_redeem, offline_predict_purchase, "")
#     
#     for learning_rate in range()
    offline_predict_redeem = offline_predict('redeem', offline_train_X_redeem, offline_train_y_redeem, offline_test_X_redeem)
#     data_compare(offline_test_y_redeem, offline_predict_redeem)
    error_plot(offline_test_y_redeem, offline_predict_redeem, "")
    
    