import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import preprocessing
from sklearn import svm
import numpy as np
import csv

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

def simple_norm(X, max_list):
    result = list()
    for i in range(len(max_list)):
        value = (X[i] - max_list[i][1]) / (max_list[i][0] - max_list[i][1])
        result.append(value)
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

def main():
    purchase_features = pd.read_csv('./data/purchase_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    redeem_features = pd.read_csv('./data/redeem_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    result = pd.read_csv('result.csv', index_col = 'time', parse_dates = 'time')

    purchase_trian_y = result['20140601':]['purchase']
    redeem_train_y = result['20140601':]['redeem']
    purchase_x = purchase_features['20140601':]
    redeem_x = redeem_features['20140601':]

    # purchase_test_y = result['20140801':]['purchase']
    # redeem_test_y = result['20140801':]['redeem']
    purchase_test_x = pd.read_csv('./data/sep_purchase_features.csv', index_col = 'report_date', parse_dates = 'report_date')
    redeem_test_x = pd.read_csv('./data/sep_redeem_features.csv', index_col = 'report_date', parse_dates = 'report_date')

    max_list_purchase, purchase_norm = normalized(purchase_x)
    max_list_redeem, redeem_norm = normalized(redeem_x)
    # purchase_y_norm = normalized_test(purchase_test_x, max_list_purchase)
    # redeem_y_norm = normalized_test(redeem_test_x, max_list_redeem)

    m1 = GradientBoostingRegressor(n_estimators=500, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=2).fit(purchase_x, purchase_trian_y)
    m2 = GradientBoostingRegressor(n_estimators=500, learning_rate=0.01, max_depth=4, random_state=0, loss='lad', min_samples_split=2).fit(redeem_x, redeem_train_y)
    y_p_pre = list()
    y_r_pre = list()
    last_value_p = purchase_trian_y[-1]
    last_value_r = redeem_train_y[-1]

    time = 20140900
    output = list()

    for i in range(30):
        time += 1
        if i != 0:
            purchase_test_x.ix[i, 'yesterday_purchase'] = last_value_p
            # purchase_test_x.ix[i, 'yesterday_redeem'] = last_value_r
            # redeem_test_x.ix[i, 'yesterday_purchase'] = last_value_p
            redeem_test_x.ix[i, 'yesterday_redeem'] = last_value_r
        if i-7 >= 0:
            purchase_test_x.ix[i, 'week1_purchase'] = y_p_pre[i-7]
            redeem_test_x.ix[i, 'week1_redeem'] = y_r_pre[i-7]
        else:
            j = str(20140825 + i)
            purchase_test_x.ix[i, 'week1_purchase'] = result.ix[j, 'purchase']
            redeem_test_x.ix[i, 'week1_redeem'] = result.ix[j, 'redeem']
        if i-14 >= 0:
            purchase_test_x.ix[i, 'week2_purchase'] = y_p_pre[i-14]
            redeem_test_x.ix[i, 'week2_redeem'] = y_r_pre[i-14]
        else:
            j = str(20140818 + i)
            purchase_test_x.ix[i, 'week2_purchase'] = result.ix[j, 'purchase']
            redeem_test_x.ix[i, 'week2_redeem'] = result.ix[j, 'redeem']
        if i-21 >= 0:
            purchase_test_x.ix[i, 'week3_purchase'] = y_p_pre[i-21]
            redeem_test_x.ix[i, 'week3_redeem'] = y_r_pre[i-21]
        else:
            j = str(20140811 + i)
            purchase_test_x.ix[i, 'week3_purchase'] = result.ix[j, 'purchase']
            redeem_test_x.ix[i, 'week3_redeem'] = result.ix[j, 'redeem']
        if i-28 >= 0:
            purchase_test_x.ix[i, 'week4_purchase'] = y_p_pre[i-28]
            redeem_test_x.ix[i, 'week4_redeem'] = y_r_pre[i-28]
        else:
            j = str(20140804 + i)
            purchase_test_x.ix[i, 'week4_purchase'] = result.ix[j, 'purchase']
            redeem_test_x.ix[i, 'week4_redeem'] = result.ix[j, 'redeem']

        test_x_p = simple_norm(purchase_test_x.ix[i].values, max_list_purchase)
        p_pre = m1.predict(test_x_p)
        last_value_p = p_pre
        print purchase_test_x.ix[i].values
        print p_pre

        test_x_r = simple_norm(redeem_test_x.ix[i].values, max_list_redeem) 
        r_pre = m2.predict(test_x_r)
        last_value_r = r_pre

        y_p_pre.append(p_pre)
        y_r_pre.append(r_pre)

        output.append((time, int(p_pre), int(r_pre)))

    csvfile = file('predict.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerows(output)
    csvfile.close()

if __name__ == '__main__':
    main()