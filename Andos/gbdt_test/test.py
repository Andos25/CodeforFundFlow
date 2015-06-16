import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import preprocessing
from sklearn import svm
import numpy as np
import datetime

def normalized(X_list):
    max_list = list()
    tmp_result = list()
    result = list()
    for i in X_list.columns:
        tmp = np.array(X_list[i])
        max_list.append((tmp.max(), tmp.min()))
        line = list()
        for j in tmp:
            value = (j - tmp.min()) / (tmp.max() - tmp.min())
            line.append(value)
        tmp_result.append(line)

    for i in range(len(tmp_result[0])):
        line = list()
        for j in range(len(tmp_result)):
            line.append(tmp_result[j][i])
        result.append(line)

    return max_list, result

def normalized_test(X_test, max_list):
    tmp_result = list()
    result = list()
    count = -1
    for i in X_test.columns:
        count += 1
        tmp = np.array(X_test[i])
        line = list()
        for j in tmp:
            value = (j - max_list[count][1]) / (max_list[count][0] - max_list[count][1])
            line.append(value)
        tmp_result.append(line)

    for i in range(len(tmp_result[0])):
        line = list()
        for j in range(len(tmp_result)):
            line.append(tmp_result[j][i])
        result.append(line)

    return result

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
    purchase_features = pd.read_csv('./data/purchase_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    redeem_features = pd.read_csv('./data/redeem_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    result = pd.read_csv('result.csv', index_col = 'time', parse_dates = 'time')

    purchase_trian_y = result['20140401':'20140630']['purchase']
    redeem_train_y = result['20140401':'20140630']['redeem']
    purchase_x = purchase_features['20140401':'20140630']
    redeem_x = redeem_features['20140401':'20140630']

    purchase_test_y = result['20140701':'20140731']['purchase']
    redeem_test_y = result['20140701':'20140731']['redeem']
    purchase_test_x = purchase_features['20140701':'20140731']
    redeem_test_x = redeem_features['20140701':'20140731']

    max_list_purchase, purchase_norm = normalized(purchase_x)
    max_list_redeem, redeem_norm = normalized(redeem_x)
    purchase_y_norm = normalized_test(purchase_test_x, max_list_purchase)
    redeem_y_norm = normalized_test(redeem_test_x, max_list_redeem)

    m1 = GradientBoostingRegressor(n_estimators=500, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=2).fit(purchase_x, purchase_trian_y)
    m2 = GradientBoostingRegressor(n_estimators=500, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=2).fit(redeem_x, redeem_train_y)

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

        p_pre = m1.predict(purchase_y_norm[i])
        # p_pre += last_value_p
        last_value_p = p_pre
        r_pre = m2.predict(redeem_y_norm[i])
        # r_pre += last_value_r
        last_value_r = r_pre

        y_p_pre.append(p_pre)
        y_r_pre.append(r_pre)

    print "purchage mean/var error", error(purchase_test_y, y_p_pre)
    print "redeem mean/var error", error(redeem_test_y, y_r_pre)

def test2():
    purchase_features = pd.read_csv('./data/purchase_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    redeem_features = pd.read_csv('./data/redeem_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    result = pd.read_csv('result.csv', index_col = 'time', parse_dates = 'time')

    purchase_trian_y = result['20140501':'20140731']['purchase']
    redeem_train_y = result['20140501':'20140731']['redeem']
    purchase_x = purchase_features['20140501':'20140731']
    redeem_x = redeem_features['20140501':'20140731']

    purchase_test_y = result['20140801':]['purchase']
    redeem_test_y = result['20140801':]['redeem']
    purchase_test_x = purchase_features['20140801':]
    redeem_test_x = redeem_features['20140801':]

    max_list_purchase, purchase_norm = normalized(purchase_x)
    max_list_redeem, redeem_norm = normalized(redeem_x)
    purchase_y_norm = normalized_test(purchase_test_x, max_list_purchase)
    redeem_y_norm = normalized_test(redeem_test_x, max_list_redeem)

    m1 = GradientBoostingRegressor(n_estimators=500, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=2).fit(purchase_x, purchase_trian_y)
    m2 = GradientBoostingRegressor(n_estimators=500, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=2).fit(redeem_x, redeem_train_y)

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
        # if i-7 >= 0:
        #     purchase_test_x.ix[i, 'week1'] = y_p_pre[i-7]
        #     redeem_test_x.ix[i, 'week1'] = y_r_pre[i-7]
        # if i-14 >= 0:
        #     purchase_test_x.ix[i, 'week2'] = y_p_pre[i-14]
        #     redeem_test_x.ix[i, 'week2'] = y_r_pre[i-14]
        # if i-21 >= 0:
        #     purchase_test_x.ix[i, 'week3'] = y_p_pre[i-21]
        #     redeem_test_x.ix[i, 'week3'] = y_r_pre[i-21]
        # if i-28 >= 0:
        #     purchase_test_x.ix[i, 'week4'] = y_p_pre[i-28]
        #     redeem_test_x.ix[i, 'week4'] = y_r_pre[i-28]

        p_pre = m1.predict(purchase_y_norm[i])
        # p_pre += last_value_p
        last_value_p = p_pre
        r_pre = m2.predict(redeem_y_norm[i])
        # r_pre += last_value_r
        last_value_r = r_pre

        y_p_pre.append(p_pre)
        y_r_pre.append(r_pre)

    print "purchage mean/var error", error(purchase_test_y, y_p_pre)
    print "redeem mean/var error", error(redeem_test_y, y_r_pre)

if __name__ == '__main__':
    test1()
    test2()



