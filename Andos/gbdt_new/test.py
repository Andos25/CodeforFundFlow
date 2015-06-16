import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import preprocessing
from sklearn import svm
import numpy as np
import datetime

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

def test1():
    purchase_features = pd.read_csv('purchase_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    redeem_features = pd.read_csv('redeem_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    result = pd.read_csv('result.csv', index_col = 'time', parse_dates = 'time')

    purchase_trian_y = result['20140401':'20140630']['purchase']
    redeem_train_y = result['20140401':'20140630']['redeem']
    purchase_x = purchase_features['20140401':'20140630']
    redeem_x = redeem_features['20140401':'20140630']

    purchase_test_y = result['20140701':'20140731']['purchase']
    redeem_test_y = result['20140701':'20140731']['redeem']
    purchase_test_x = purchase_features['20140701':'20140731']
    redeem_test_x = redeem_features['20140701':'20140731']

    purchase_delta = delta(purchase_trian_y)
    redeem_delta = delta(redeem_train_y)

    m1 = GradientBoostingRegressor(n_estimators=350, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=2).fit(purchase_x.values, purchase_trian_y)
    m2 = GradientBoostingRegressor(n_estimators=350, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=2).fit(redeem_x.values, redeem_train_y)

    y_p_pre = list()
    y_r_pre = list()
    last_value_p = purchase_trian_y[-1]
    last_value_r = redeem_train_y[-1]

    for i in range(31):
        if i != 0:
            purchase_test_x.ix[i, 'yesterday_purchase'] = last_value_p
            purchase_test_x.ix[i, 'yesterday_redeem'] = last_value_r
            redeem_test_x.ix[i, 'yesterday_purchase'] = last_value_p
            redeem_test_x.ix[i, 'yesterday_redeem'] = last_value_r
        if i-7 >= 0:
            purchase_test_x.ix[i, 'week1'] = y_p_pre[i-7]
            redeem_test_x.ix[i, 'week1'] = y_r_pre[i-7]
        if i-14 >= 0:
            purchase_test_x.ix[i, 'week2'] = y_p_pre[i-14]
            redeem_test_x.ix[i, 'week2'] = y_r_pre[i-14]
        if i-21 >= 0:
            purchase_test_x.ix[i, 'week3'] = y_p_pre[i-21]
            redeem_test_x.ix[i, 'week3'] = y_r_pre[i-21]
        if i-28 >= 0:
            purchase_test_x.ix[i, 'week4'] = y_p_pre[i-28]
            redeem_test_x.ix[i, 'week4'] = y_r_pre[i-28]

        p_pre = m1.predict(purchase_test_x.ix[i].values)
        # p_pre += last_value_p
        last_value_p = p_pre
        r_pre = m2.predict(redeem_test_x.ix[i].values)
        # r_pre += last_value_r
        last_value_r = r_pre

        y_p_pre.append(p_pre)
        y_r_pre.append(r_pre)

    print "purchage mean/var error", error(purchase_test_y, y_p_pre)
    print "redeem mean/var error", error(redeem_test_y, y_r_pre)

def test2():
    purchase_features = pd.read_csv('purchase_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    redeem_features = pd.read_csv('redeem_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    result = pd.read_csv('result.csv', index_col = 'time', parse_dates = 'time')

    purchase_trian_y = result['20140501':'20140731']['purchase']
    redeem_train_y = result['20140501':'20140731']['redeem']
    purchase_x = purchase_features['20140501':'20140731']
    redeem_x = redeem_features['20140501':'20140731']

    purchase_test_y = result['20140801':]['purchase']
    redeem_test_y = result['20140801':]['redeem']
    purchase_test_x = purchase_features['20140801':]
    redeem_test_x = redeem_features['20140801':]

    purchase_delta = delta(purchase_trian_y)
    redeem_delta = delta(redeem_train_y)
    m1 = GradientBoostingRegressor(n_estimators=350, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=2).fit(purchase_x.values, purchase_trian_y)
    m2 = GradientBoostingRegressor(n_estimators=350, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=2).fit(redeem_x.values, redeem_train_y)

    y_p_pre = list()
    y_r_pre = list()
    last_value_p = purchase_trian_y[-1]
    last_value_r = redeem_train_y[-1]

    for i in range(31):
        if i != 0:
            purchase_test_x.ix[i, 'yesterday_purchase'] = last_value_p
            purchase_test_x.ix[i, 'yesterday_redeem'] = last_value_r
            redeem_test_x.ix[i, 'yesterday_purchase'] = last_value_p
            redeem_test_x.ix[i, 'yesterday_redeem'] = last_value_r
        if i-7 >= 0:
            purchase_test_x.ix[i, 'week1'] = y_p_pre[i-7]
            redeem_test_x.ix[i, 'week1'] = y_r_pre[i-7]
        else:
            j = str(20140725 + i)
            purchase_test_x.ix[i, 'week1'] = result.ix[j, 'purchase']
            redeem_test_x.ix[i, 'week1'] = result.ix[j, 'redeem']
        if i-14 >= 0:
            purchase_test_x.ix[i, 'week2'] = y_p_pre[i-14]
            redeem_test_x.ix[i, 'week2'] = y_r_pre[i-14]
        else:
            j = str(20140718 + i)
            purchase_test_x.ix[i, 'week2'] = result.ix[j, 'purchase']
            redeem_test_x.ix[i, 'week2'] = result.ix[j, 'redeem']
        if i-21 >= 0:
            purchase_test_x.ix[i, 'week3'] = y_p_pre[i-21]
            redeem_test_x.ix[i, 'week3'] = y_r_pre[i-21]
        else:
            j = str(20140711 + i)
            purchase_test_x.ix[i, 'week3'] = result.ix[j, 'purchase']
            redeem_test_x.ix[i, 'week3'] = result.ix[j, 'redeem']
        if i-28 >= 0:
            purchase_test_x.ix[i, 'week4'] = y_p_pre[i-28]
            redeem_test_x.ix[i, 'week4'] = y_r_pre[i-28]
        else:
            j = str(20140704 + i)
            purchase_test_x.ix[i, 'week4'] = result.ix[j, 'purchase']
            redeem_test_x.ix[i, 'week4'] = result.ix[j, 'redeem']

        p_pre = m1.predict(purchase_test_x.ix[i].values)
        # p_pre += last_value_p
        last_value_p = p_pre
        r_pre = m2.predict(redeem_test_x.ix[i].values)
        # r_pre += last_value_r
        last_value_r = r_pre

        y_p_pre.append(p_pre)
        y_r_pre.append(r_pre)

    print "purchage mean/var error", error(purchase_test_y, y_p_pre)
    print "redeem mean/var error", error(redeem_test_y, y_r_pre)

if __name__ == '__main__':
    test1()
    test2()



