# coding=UTF-8
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats.mstats import zscore

# ['Interest_O_N', 'Interest_1_W', 'Interest_2_W', 'Interest_1_M', 'Interest_3_M', 'Interest_6_M', 'Interest_9_M', 'Interest_1_Y']

tianchi_path = '/home/lt/data/tianchi/'
cleaned_path = tianchi_path + 'cleaned/'
stat_path = tianchi_path + 'stat/'
pearson_outputpath = stat_path + 'after_201404_pearson.csv'

def normalize(data):
    for column in data.columns:
        data[column] = zscore(data[column])
    return data

# calculate pearson's correlation coefficient of each 2 of data columns
def pearson_cor(data):
    out = open(pearson_outputpath, 'w')
    for col1 in data.columns:
        for col2 in data.columns:
            [coef, p_value] = pearsonr(data[col1], data[col2])
            out.write(col1+'*'+col2+','+str(coef) + ',' + str(p_value)+'\n')
    out.close()
    
if __name__ == '__main__':
    purchase = pd.read_csv(cleaned_path+'purchase_by_day.csv', header=0, parse_dates='report_date', index_col='report_date').ix[274:]
    redeem = pd.read_csv(cleaned_path+'redeem_by_day.csv', header=0, parse_dates='report_date', index_col='report_date').ix[274:]
    intervel = 7
    print pearsonr(purchase[:-intervel], redeem[intervel:])
#     interest = pd.read_csv(tianchi_path + 'mfd_day_share_interest.csv')
#     redeem.plot()
#     plt.show()
#     print pearsonr(purchase['total_purchase_amt'], data['day_of_week'].values)
