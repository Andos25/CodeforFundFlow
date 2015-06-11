import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import preprocessing
from sklearn import svm
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

def main():
    purchase_features = pd.read_csv('purchase_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    redeem_features = pd.read_csv('redeem_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    result = pd.read_csv('result.csv', index_col = 'time', parse_dates = 'time')

    purchase_trian_y = result['20140430':]['purchase']
    redeem_train_y = result['20140430':]['redeem']
    purchase_x = purchase_features['20140501':]
    redeem_x = redeem_features['20140501':]

    # purchase_test_y = result['20140801':]['purchase']
    # redeem_test_y = result['20140801':]['redeem']
    purchase_test_x = pd.read_csv('sep_purchase_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    redeem_test_x = pd.read_csv('sep_redeem_features.csv', index_col = 'report_date', parse_dates = 'report_date')

    purchase_delta = delta(purchase_trian_y)
    redeem_delta = delta(redeem_train_y)

    m1 = GradientBoostingRegressor(n_estimators=2500, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=3).fit(purchase_x.values, purchase_delta)
    m2 = GradientBoostingRegressor(n_estimators=2500, learning_rate=0.01, max_depth=3, random_state=0, loss='lad', min_samples_split=2).fit(redeem_x.values, redeem_delta)

    y_p_pre = list()
    y_r_pre = list()
    last_value_p = purchase_trian_y[-1]
    last_value_r = redeem_train_y[-1]

    time = 20140900
    result = list()

    for i in range(30):
        time += 1
        if i != 0:
            purchase_test_x.ix[i, 'yesterday_purchase'] = last_value_p
            purchase_test_x.ix[i, 'yesterday_redeem'] = last_value_r
            redeem_test_x.ix[i, 'yesterday_purchase'] = last_value_p
            redeem_test_x.ix[i, 'yesterday_redeem'] = last_value_r
        if i-7 >= 0:
            purchase_test_x.ix[i, 'week1'] = y_p_pre[i-7]
            redeem_test_x.ix[i, 'week1'] = y_r_pre[i-7]
        else:
            purchase_test_x.ix[i, 'week1'] = purchase_trian_y.ix[j, 'week1']
            redeem_test_x.ix[i, 'week1'] = purchase_trian_y.ix[j, 'week1']
        if i-14 >= 0:
            j = str(20140825 + i)
            purchase_test_x.ix[i, 'week2'] = y_p_pre[i-14]
            redeem_test_x.ix[i, 'week2'] = y_r_pre[i-14]
        else:
            j = str(20140818 + i)
            purchase_test_x.ix[i, 'week2'] = purchase_trian_y.ix[j, 'week2']
            redeem_test_x.ix[i, 'week2'] = purchase_trian_y.ix[j, 'week2']
        if i-21 >= 0:
            purchase_test_x.ix[i, 'week3'] = y_p_pre[i-21]
            redeem_test_x.ix[i, 'week3'] = y_r_pre[i-21]
        else:
            purchase_test_x.ix[i, 'week3'] = purchase_trian_y.ix[j, 'week3']
            redeem_test_x.ix[i, 'week3'] = purchase_trian_y.ix[j, 'week3']
        if i-28 >= 0:
            purchase_test_x.ix[i, 'week4'] = y_p_pre[i-28]
            redeem_test_x.ix[i, 'week4'] = y_r_pre[i-28]
        else:
            j = str(20140804 + i)
            purchase_test_x.ix[i, 'week4'] = purchase_trian_y.ix[j, 'week4']
            redeem_test_x.ix[i, 'week4'] = purchase_trian_y.ix[j, 'week4']

        print purchase_test_x.ix[i]
        p_pre = m1.predict(purchase_test_x.ix[i].values)
        p_pre += last_value_p
        last_value_p = p_pre
        r_pre = m2.predict(redeem_test_x.ix[i].values)
        r_pre += last_value_r
        last_value_r = r_pre

        y_p_pre.append(p_pre)
        y_r_pre.append(r_pre)

        result.append((time, int(p_pre), int(r_pre)))

    csvfile = file('predict.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerows(result)
    csvfile.close()

if __name__ == '__main__':
    main()