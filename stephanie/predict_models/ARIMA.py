# coding=UTF-8
import pandas as pd
import matplotlib.pyplot as plt
from predict_models.metrics import data_compare, error_plot
from statsmodels.tsa import arima_model

purchase_order = [7,1,5]
redeem_order = [5,1,5]

cleaned = '/home/lt/data/tianchi/cleaned/'
arima_gbdt = cleaned+'arima_gbdt/'

# 20130701~20140831
purchase = pd.read_csv(cleaned+'purchase_by_day.csv', header=0, parse_dates='report_date', index_col='report_date')
redeem = pd.read_csv(cleaned+'redeem_by_day.csv', header=0, parse_dates='report_date', index_col='report_date')

def autocorrelation_analysis(origin_df):
    plt.plot(origin_df[184:], label='0')
    order1 = origin_df.diff(1)
    plt.plot(order1[184:], label='1')
    plt.legend()
    plt.show()

def arima_modeling(train, order, predict_start, predict_end):
    model = arima_model.ARIMA(train, order)
    arima_res = model.fit(maxiter=200)
    print arima_res.summary()
    predict = arima_res.predict(predict_start, predict_end, typ='levels')
    return predict

def predict(predict_type):
    if type == 'purchase':
        # start from 201405
        predict = arima_modeling(purchase.ix[304:], purchase_order, '20140901', '20140930')
        predict.round().to_csv('/home/lt/data/tianchi/tmp_pur.csv')
    elif type == 'redeem':
        # start from 201405
        predict = arima_modeling(redeem.ix[304:], redeem_order, '20140901', '20140930')
        predict.round().to_csv('/home/lt/data/tianchi/tmp_red.csv')
    else:
        print 'wrong type'
        
if __name__ == '__main__':
##########################################################################################
# predict
#     predict('purchase')
#     predict('redeem')
#     print purchase.ix[288]
##########################################################################################
# without exog
    predict = arima_modeling(redeem.ix[274:], redeem_order, '20140901','20140930')
#     residual = redeem.ix[274:] - predict
#     error_plot(redeem.ix[274:], predict, '')
    predict.to_csv(arima_gbdt+'sep_redeem_by_day.csv')
#     predict.plot()
#     plt.show()
    
    