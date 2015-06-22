import pandas as pd
from sklearn import ensemble
import matplotlib.pyplot as plt
# from sklearn.ensemble import GradientBoostingRegressor

from metrics import data_compare, error_plot, get_metrics, residual_analysis, relative_error
import numpy as np
import csv

def error(Y1, Y2):
    result = list()
    count = 0
    for i in range(len(Y1)):
        value = abs(Y1[i]-Y2[i])/Y1[i]
        if value <= 0.3:
            count += 1
        result.append(value)
    print count
    values = np.array(result)
    return values.mean(), values.var()

def delta(origin):
    delta = pd.Series(index = origin.index)
    delta = delta[1 : ]
    for i in range(0, delta.size):
        delta[i] = origin[i + 1] - origin[i]
    return delta

wd = "../new/"
purchase_features = pd.read_csv(wd + 'purchase_features.csv', index_col = 'report_date', parse_dates = 'report_date')
redeem_features = pd.read_csv(wd + 'redeem_features.csv', index_col = 'report_date', parse_dates = 'report_date')
daily_summary = pd.read_csv(wd + 'daily_summary.csv', index_col = 'report_date', parse_dates = 'report_date')

sep_purchase_features = pd.read_csv(wd + 'sep_purchase_features.csv', index_col = 'report_date', parse_dates = 'report_date')
sep_redeem_features = pd.read_csv(wd + 'sep_redeem_features.csv', index_col = 'report_date', parse_dates = 'report_date')


#offline
offline_during = {'train_start':'20140401', 'train_end':'20140731', 'test_start':'20140801', 'test_end':'20140831'}
offline_train_X_purchase = purchase_features[offline_during['train_start']:offline_during['train_end']]
offline_train_X_redeem = redeem_features[offline_during['train_start']:offline_during['train_end']]
offline_train_y_purchase = daily_summary[offline_during['train_start']:offline_during['train_end']]['total_purchase_amt']
offline_train_y_redeem = daily_summary[offline_during['train_start']:offline_during['train_end']]['total_redeem_amt']
offline_test_X_purchase = purchase_features[offline_during['test_start']:offline_during['test_end']]
offline_test_X_redeem = redeem_features[offline_during['test_start']:offline_during['test_end']]
offline_test_y_purchase = daily_summary[offline_during['test_start']:offline_during['test_end']]['total_purchase_amt']
offline_test_y_redeem = daily_summary[offline_during['test_start']:offline_during['test_end']]['total_redeem_amt']


#online
online_during = {'train_start':'20140401', 'train_end':'20140831', 'test_start':'20140901', 'test_end':'20140930'}
online_train_X_purchase = purchase_features[online_during['train_start']:online_during['train_end']]
online_train_X_redeem = redeem_features[online_during['train_start']:online_during['train_end']]
online_train_y_purchase = daily_summary[online_during['train_start']:online_during['train_end']]['total_purchase_amt']
online_train_y_redeem = daily_summary[online_during['train_start']:online_during['train_end']]['total_redeem_amt']

online_test_X_purchase = sep_purchase_features[online_during['test_start']:online_during['test_end']]
online_test_X_redeem = sep_redeem_features[online_during['test_start']:online_during['test_end']]

#115: 639, 1, 0.01        665, 3,0.02

#523 1 0.01
purchase_params = {'n_estimators':523, 'max_depth':1, 'random_state':0, 'min_samples_split':2,
                   'learning_rate':0.01, 'loss':'lad'}
#998 1 0.02
redeem_params = {'n_estimators':998, 'max_depth':1, 'random_state':0, 'min_samples_split':4,
                 'learning_rate':0.02, 'loss':'lad'}


def fill_features(date, sep, sep_purchase, sep_redeem, relativedays=0):
    yesterday = date - 1
    if yesterday in sep:
        online_test_X_purchase.ix[date, 'yesterday_purchase'] = sep_purchase.ix[yesterday, 'total_purchase_amt']
        online_test_X_purchase.ix[date, 'yesterday_redeem'] = sep_redeem.ix[yesterday, 'total_redeem_amt']
        online_test_X_redeem.ix[date,'yesterday_purchase'] = sep_purchase.ix[yesterday, 'total_purchase_amt']
        online_test_X_redeem.ix[date,'yesterday_redeem'] = sep_redeem.ix[yesterday, 'total_redeem_amt']
    else:
        online_test_X_purchase.ix[date, 'yesterday_purchase'] = online_train_y_purchase.ix[yesterday, 'total_purchase_amt']
        online_test_X_purchase.ix[date, 'yesterday_redeem'] = online_train_y_redeem.ix[yesterday, 'total_redeem_amt']
        online_test_X_redeem.ix[date,'yesterday_purchase'] = online_train_y_purchase.ix[yesterday, 'total_purchase_amt']
        online_test_X_redeem.ix[date,'yesterday_redeem'] = online_train_y_redeem.ix[yesterday, 'total_redeem_amt']

    online_test_X_purchase.ix[date, 'relative_days'] = relativedays
    online_test_X_redeem.ix[date, 'relative_days'] = relativedays


    # for i in range(1,8):
    #     date0 = date - i
    #     if date0 in sep:
    #         online_test_X_purchase.ix[date, 'attr' + str(i)] = sep_purchase.ix[date0, 'total_purchase_amt'] - \
    #                                                            sep_redeem.ix[date0, 'total_redeem_amt']
    #         online_test_X_redeem.ix[date, 'attr' + str(i)] = sep_purchase.ix[date0, 'total_purchase_amt'] - \
    #                                                          sep_redeem.ix[date0, 'total_redeem_amt']
    #
    #     else:
    #         online_test_X_purchase.ix[date, 'attr' + str(i)] = online_train_y_purchase.ix[date0, 'total_purchase_amt'] - \
    #                                                            online_train_y_redeem.ix[date0, 'total_redeem_amt']
    #         online_test_X_redeem.ix[date, 'attr' + str(i)] = online_train_y_purchase.ix[date0, 'total_purchase_amt'] - \
    #                                                          online_train_y_redeem.ix[date0, 'total_redeem_amt']




def do_week(weeknum, sep, date, sep_purchase, sep_redeem, col_name1):
    if weeknum in sep:
        online_test_X_purchase.ix[date, col_name1+'_purchase'] = sep_purchase.ix[weeknum, 'total_purchase_amt']
        online_test_X_redeem.ix[date, col_name1+'_redeem'] = sep_redeem.ix[weeknum, 'total_redeem_amt']
    else:
        online_test_X_purchase.ix[date, col_name1+'_purchase'] = online_train_y_purchase.ix[weeknum, 'total_purchase_amt']
        online_test_X_redeem.ix[date, col_name1+'_redeem'] = online_train_y_redeem.ix[weeknum, 'total_redeem_amt']

def online_predict():
    purchase_clf = ensemble.GradientBoostingRegressor(**purchase_params).fit(online_train_X_purchase, online_train_y_purchase)
    redeem_clf = ensemble.GradientBoostingRegressor(**redeem_params).fit(online_train_X_redeem, online_train_y_redeem)
    sep = pd.date_range('20140901', '20140930', freq='D')
    sep_purchase = pd.DataFrame(index=sep)
    sep_redeem = pd.DataFrame(index=sep)
    i = 0
    for date in sep:
        relativedays = 61 + i/7
        # print relativedays
        i+=1
        fill_features(date, sep, sep_purchase, sep_redeem, relativedays)
        do_week(date -7, sep, date, sep_purchase, sep_redeem, 'week1')
        do_week(date -14, sep, date, sep_purchase, sep_redeem, 'week2')
        do_week(date -21, sep, date, sep_purchase, sep_redeem, 'week3')
        do_week(date -28, sep, date, sep_purchase, sep_redeem, 'week4')
        print online_test_X_purchase.ix[date]
        today_pur = purchase_clf.predict(online_test_X_purchase.ix[date])
        today_red = redeem_clf.predict(online_test_X_redeem.ix[date])
        sep_purchase.ix[date, 'total_purchase_amt'] = today_pur
        sep_redeem.ix[date, 'total_redeem_amt'] = today_red


    drop4absort5 = lambda f : str(int(round(f)))
    results = []
    origin = 20140901
    for date in sep:
        result = (str(origin), drop4absort5(sep_purchase.ix[date, 'total_purchase_amt']), drop4absort5(sep_redeem.ix[date, 'total_redeem_amt']))
        results.append(result)
        origin +=1
        print origin,drop4absort5(sep_purchase.ix[date, 'total_purchase_amt']), drop4absort5(sep_redeem.ix[date, 'total_redeem_amt'])

    fout = open('../new/result0622.csv', 'w')
    fout.write('\n'.join([','.join(result) for result in results]))
    fout.close()

    sep_purchase.to_csv('../data/online/result/tmp_pur.csv')
    sep_redeem.to_csv('../data/online/result/tmp_red.csv')


def offline_predict(predict_type, X_train, y_train, X_test):
    X_train = X_train.iloc[:,:]
    X_test = X_test.iloc[:,:]
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



def main():
    # select_params('purchase', 'max_depth', np.arange(1, 8))
    # select_params('purchase', 'n_estimators', np.arange(5, 1000, 1))
    # select_params('purchase', 'learning_rate', np.arange(0.01, 0.60, 0.01))

    # select_params('purchase', 'min_samples_split', np.arange(1,20))

    # select_params('redeem', 'n_estimators', np.arange(5, 1000, 1))
    # select_params('redeem', 'learning_rate', np.arange(0.01, 0.60, 0.01))
    # select_params('redeem', 'max_depth', np.arange(1, 8))
    # select_params('redeem', 'min_samples_split', np.arange(1,20))


    # offline
    # offline_predict_purchase = offline_predict('redeem', offline_train_X_purchase, offline_train_y_purchase, offline_test_X_purchase)
    # print relative_error(offline_test_y_purchase, offline_predict_purchase)
    # error_plot(offline_test_y_purchase, offline_predict_purchase, "")
    # residual_analysis(offline_test_y_purchase, offline_predict_purchase)

    # online
    online_predict()

if __name__ == '__main__':
    main()