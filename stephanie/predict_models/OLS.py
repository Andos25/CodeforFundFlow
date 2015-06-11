# coding=UTF-8
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from predict_models import metrics

from predict_models.metrics import error_plot

def predict(model_res, X_test, y_test):
    predictions = model_res.predict(X_test)
    print 'size of test samples: ', len(y_test), '   size of predictions: ', len(predictions)
    errors = metrics.relative_error(y_test, predictions)
    print "size of errors less than 0.3: ", len(errors), "errors: ", errors
    
def output(outputPath, purchase_sep, redeem_sep):
    out = open(outputPath, 'w')
    dates = pd.date_range('20140901', '20140930', freq='D')
    for i in range(len(dates)):
        out.write(str(dates[i])+','+str(int(round(purchase_sep[i])))+','+str(int(round(redeem_sep[i])))+'\n')
    out.close()
    
if __name__ == '__main__':
    # read data
    origin_series = pd.read_csv('/home/lt/data/tianchi/origin_series.csv', header=0, index_col=0, parse_dates=0)
    redeem_by_day = pd.read_csv('/home/lt/data/tianchi/redeem_by_day.csv', header=0, index_col=0, parse_dates=0)
    data = pd.read_table('/home/lt/data/tianchi/merged_data.csv', sep=',', header=0, index_col=0, parse_dates=0)
#     sep = pd.read_table('/home/lt/data/tianchi/余额宝_拆借率201409.csv', sep=',', header=0, parse_dates=0)
#     X_sep = sep.loc[:,['mfd_daily_yield',
#                     'mfd_7daily_yield',
#                     'Interest_O_N',
#                     'Interest_1_W',
#                     'Interest_2_W',
#                     'Interest_1_M',
#                     'Interest_3_M',
#                     'Interest_6_M',
#                     'Interest_9_M',
#                     'Interest_1_Y']]
#     X_sep = sm.add_constant(X_sep)
    
    
    purchase = data['purchase']
    redeem = data['redeem']
    X = data.loc[:,['mfd_daily_yield',
                    'mfd_7daily_yield',
                    'Interest_O_N',
                    'Interest_1_W',
                    'Interest_2_W',
                    'Interest_1_M',
                    'Interest_3_M',
                    'Interest_6_M',
                    'Interest_9_M',
                    'Interest_1_Y']]
    X = sm.add_constant(X)
    X_train, X_test = X[:369], X[396:]
    purchase_train, purchase_test = purchase[:369], purchase[396:]
    redeem_train, redeem_test = redeem[:369], redeem[396:]
    
    # purchase model
    purchase_model = sm.OLS(purchase_train, X_train)
    purchase_res = purchase_model.fit()
#     pur_sep = purchase_res.predict(X_sep)
    print purchase_res.summary()
    error_plot(purchase_res, purchase_train)
    predict(purchase_res, X_test, purchase_test)
    
    
    # redeem model
    redeem_model = sm.OLS(redeem_train, X_train)
    redeem_res = redeem_model.fit()
#     red_sep = redeem_res.predict(X_sep)
    print redeem_res.summary()
    error_plot(redeem_res, redeem_train)
    predict(redeem_res, X_test, redeem_test)

#     output('/home/lt/data/tianchi/tc_comp_predict_table.csv', pur_sep, red_sep)