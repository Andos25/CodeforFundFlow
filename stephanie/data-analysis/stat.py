# coding=UTF-8
import pandas as pd
import matplotlib.pyplot as plt

tianchi = '/home/lt/data/tianchi/'
stat = tianchi + 'stat/'
cleaned_path = tianchi + 'cleaned/'
by_user = tianchi + 'by_user/'

def group_and_save(user_profile):
    user_balance = pd.read_csv(tianchi + 'user_balance_table.csv', header=0, index_col='user_id', parse_dates='report_date')
    user_profile.groupby('sex').count().to_csv(stat + 'group_sex.csv')
    user_profile.groupby('city').count().to_csv(stat + 'group_city.csv')
    user_profile.groupby('constellation').count().to_csv(stat + 'group_constellation.csv')
    
def sep_noise_user():
    user_mean_std = pd.read_csv(stat+'user_purchase_redeem_mean_std.csv', header=0).fillna("null")
    print "total user: ", len(user_mean_std)
    record1 = user_mean_std[(user_mean_std['purchase_std']=="null") & (user_mean_std['redeem_std']=="null")]
    print "only 1 record user: ", len(record1)
    single_tranx = record1[(record1['purchase_mean']>0) | (record1['redeem_mean']>0)]
    print "only 1 tranx user: ", len(single_tranx)
    single_tranx.to_csv(stat+'singular_tranx.csv')
    
    balance = pd.read_csv(tianchi+'user_balance_table.csv', header=0, parse_dates='report_date')
    cleaned = balance[~balance['user_id'].isin(single_tranx['user_id'])]
    new_pur = cleaned.groupby('report_date')['total_purchase_amt'].sum()
    new_red = cleaned.groupby('report_date')['total_redeem_amt'].sum()
    new_pur.to_csv(cleaned_path+'purchase_by_day.csv')
    new_red.to_csv(cleaned_path+'redeem_by_day.csv')
    
def tuhao_diaosi():
    balance = pd.read_csv(tianchi + 'user_balance_table.csv', header=0, parse_dates='report_date')

#     ##############################################################################################
#     # 根据直接购买量区分用户阶层
#     # 直接购买过的记录
#     direct_balance = balance[balance['direct_purchase_amt']>0]
#     # 每个用户直接购买过的记录
#     direct_ugrp = direct_balance.groupby('user_id')
#     direct_ugrp['direct_purchase_amt'].count().to_csv(stat+'direct_purchase_count.csv')

    direct = pd.read_csv('/home/lt/data/tianchi/stat/direct_purchase_mean.csv', header=0)
    # 平均直接购买数额大于5千的算土豪
    tuhao = direct[direct['direct_purchase_mean']>=500000]['user_id']
    tuhao_balance = balance[balance['user_id'].isin(tuhao)]
    pingmin_balance = balance[~balance['user_id'].isin(tuhao)]
#     plt.plot(tuhao_balance.groupby('report_date')['total_purchase_amt'].sum())
    plt.plot(pingmin_balance.groupby('report_date')['total_purchase_amt'].sum())
    plt.plot(pingmin_balance.groupby('report_date')['total_redeem_amt'].sum())
#     plt.legend(['tuhao','pingmin'])
    plt.show()
    tuhao_balance.to_csv(by_user + 'tuhao_balance.csv', index=False)
    pingmin_balance.to_csv(by_user + 'pingmin_balance.csv')
    user = pd.read_csv('/home/lt/data/tianchi/user_profile_table.csv',header=0)
    tuhao_profile = user[user['user_id'].isin(tuhao)]

def user_by_month():
    user_balance = pd.read_csv(tianchi + 'user_balance_table.csv', header=0, parse_dates='report_date')
    grp_date = user_balance.groupby("report_date")
    
    
if __name__ == '__main__':
    tuhao_diaosi()
