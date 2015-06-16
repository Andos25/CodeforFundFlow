# coding=UTF-8
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

tianchi = '/home/lt/data/tianchi/'
cleaned_path = tianchi + 'cleaned/'
predict_path = tianchi + 'predict/'
pur_path = cleaned_path + 'purchase_by_day.csv'
red_path = cleaned_path + 'redeem_by_day.csv'
feature_output_path = tianchi + 'features_tmp.csv'
# 由于offline和online都是20140401之后的数据，所以2013年的不管
holidays = pd.to_datetime(['20140101',#元旦
            '20140131', '20140201', '20140202', '20140203', '20140204', '20140205', '20140206',#春节
            '20140405','20140406','20140407',#清明
            '20140501','20140502','20140503',#劳动
            '20140531','20140601','20140602',#端午
            '20140906','20140907','20140908',#中秋
            '20141001','20141002','20141003','20141004','20141005','20141006','20141007'])#国庆
# 本来是周末，但因节假日调休而要上班的日子
tiaoxiu = pd.to_datetime(['20140126', '20140208', '20140504', '20140928', '20141011'])

def isholiday_feature():
    out = open(feature_output_path, 'w')
    dates = pd.date_range('20140401','20140930',freq='D')
    for i in range(len(dates)):
        isholiday = 0
        curday = pd.to_datetime(str(dates[i])).strftime('%Y%m%d')
        if curday in holidays: 
            print curday
            isholiday = 1
        out.write(curday + ',' + str(isholiday) + '\n')
    out.close()
    
def is_tiaoxiu():
    out = open(feature_output_path, 'w')
    dates = pd.date_range('20140401','20140930',freq='D')
    for i in range(len(dates)):
        istiaoxiu = 0
        curday = pd.to_datetime(str(dates[i])).strftime('%Y%m%d')
        if curday in tiaoxiu: 
            print curday
            istiaoxiu = 1
        out.write(curday + ',' + str(istiaoxiu) + '\n')
    out.close()
    
def shouldwork_feature():
    out = open(feature_output_path, 'w')
    dates = pd.date_range('20140401','20140930',freq='D')
    dayofweek = dates.dayofweek + 1
    for i in range(len(dates)):
        shouldwork = 1
        curday = pd.to_datetime(str(dates[i])).strftime('%Y%m%d')
        if (dayofweek[i]>5 and (curday not in tiaoxiu)) or (curday in holidays): 
            print curday
            shouldwork = 0
        out.write(curday + ',' + str(shouldwork) + '\n')
    out.close()

def dummy_weekday():
    out = open(feature_output_path, 'w')
    dates = pd.date_range('20130701','20140930',freq='D')
    dayofweek = dates.dayofweek + 1
    for i in range(len(dates)):
        print dates[i], dayofweek[i]
        curday = pd.to_datetime(str(dates[i])).strftime('%Y%m%d')
        if dayofweek[i] == 1: 
            out.write(curday + ',' + '1,0,0,0,0,0,0' + '\n')
        elif dayofweek[i] == 2: 
            out.write(curday + ',' + '0,1,0,0,0,0,0' + '\n')
        elif dayofweek[i] == 3: 
            out.write(curday + ',' + '0,0,1,0,0,0,0' + '\n')
        elif dayofweek[i] == 4: 
            out.write(curday + ',' + '0,0,0,1,0,0,0' + '\n')
        elif dayofweek[i] == 5: 
            out.write(curday + ',' + '0,0,0,0,1,0,0' + '\n')
        elif dayofweek[i] == 6: 
            out.write(curday + ',' + '0,0,0,0,0,1,0' + '\n')
        elif dayofweek[i] == 7: 
            out.write(curday + ',' + '0,0,0,0,0,0,1' + '\n')
    out.close()

def percentile_dayofmanth():
    out = open(feature_output_path, 'w')
    dates = pd.date_range('20140401','20140930',freq='D')
    dayofmonth = dates.day
    monthday = dates.daysinmonth
    for i in range(len(dates)):
        percent = float(dayofmonth[i])/monthday[i]
        curday = pd.to_datetime(str(dates[i])).strftime('%Y%m%d')
        out.write(curday + ',' + str(percent) + '\n')
    out.close()
    
def other_day_feature(gen_type):
    filepath = ''
    if gen_type == 'purchase':
        filepath = pur_path
    elif gen_type == 'redeem':
        filepath = red_path
    else:
        print 'wrong type'
    data = pd.read_csv(filepath, header=0, parse_dates='report_date', index_col='report_date')
    date_index = data.index
    data.ix[pd.Series(index=date_index).tshift(periods=-28, freq='D').index].to_csv(feature_output_path)
        
def percent_in_term():
    shouldwork = pd.read_csv(cleaned_path+'sep_purchase_features.csv', header=0)['shouldwork']
    print shouldwork
    count = []
    day_type = 1
    count_i = 0
    for i in range(len(shouldwork)):
        if day_type != shouldwork[i]:
            count.append(count_i)
            day_type = shouldwork[i]
            count_i = 1
        else:
            count_i += 1
    count.append(count_i)
    print count
    j = 0
    start_i = 1
    percent = []
    day_index = 1
    for i in range(len(shouldwork)):
        if shouldwork[i] != start_i:
            j += 1
            day_index = 1
            start_i = shouldwork[i]
        percent.append(float(day_index)/count[j])
        day_index += 1
    pd.DataFrame(percent).to_csv(feature_output_path, index=False)
    
if __name__ == '__main__':
#     print holidays, tiaoxiu
    percent_in_term()
    