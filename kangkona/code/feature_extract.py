#!/usr/bin/python
# -*- coding: utf-8 -*-
 
__author__ = 'kangkona'

import pandas as pd


diff = lambda j, pr_list, p_or_r:(pr_list[j][1] - pr_list[j][2])*1.0
phrchase_diff = lambda pr_list, j : diff(j, pr_list, 1)
redeem_diff = lambda pr_list, j : diff(j, pr_list, 2)

add = lambda j, pr_list, p_or_r:(pr_list[j][1] + pr_list[j][2])*1.0
phrchase_add = lambda pr_list, j : diff(j, pr_list, 1)
redeem_add = lambda pr_list, j : diff(j, pr_list, 2)

#从资金流动的角度提取的特征
#pr_tuples: (date, phrchase, redeem)
def features_about_flow(pr_list, i):
    features = [0 for k in range(7)]
    if i >= 8:
        features = []
        for j in range(i-1, i-8, -1):
            feature = [pr_list[j][1] - pr_list[j][2]]
            features = features + feature
        return tuple(features), tuple(features)
    else:
        return tuple(features), tuple(features)


def extract(pr_file, phrchase_file, redeem_file):
    pr_total = pd.read_csv(pr_file, parse_dates = 'report_date')
    pr_list = [(pr_total.report_date[i], pr_total.total_purchase_amt[i], pr_total.total_redeem_amt[i]) \
               for i in range(len(pr_total.total_purchase_amt))]
    phrchase_features = []
    redeem_features = []
    for i in range(len(pr_list)):
        p, r = features_about_flow(pr_list, i)
        phrchase_features.append(p)
        redeem_features.append(r)
    
    relative_growth_rates = ["attr" + str(i) for i in range(1, 8)]
    fout_phrchase = open(phrchase_file, "w")
    fout_phrchase.write(','.join(relative_growth_rates) + '\n')
    fout_phrchase.write('\n'.join([','.join([str(pfa) for pfa in pf]) for pf in phrchase_features]))
    fout_phrchase.close()

    fout_redeem = open(redeem_file, "w")
    fout_redeem.write(','.join(relative_growth_rates) + '\n')
    fout_redeem.write('\n'.join([','.join([str(rfa) for rfa in rf]) for rf in redeem_features]))
    fout_redeem.close()

def merge_features(old_features_file, new_feature_file, merge_file):
    f_old = open(old_features_file)
    f_new = open(new_feature_file)
    f_out = open(merge_file, "w")
    while True:
        line_old = f_old.readline()
        line_new = f_new.readline()
        if not line_old or not line_new:
            break
        f_out.write(line_old.strip() + ',' +  line_new)
    f_out.close()
    f_new.close()
    f_old.close()

def main():
    extract("../../features/purchase_by_day.csv", "../data/pf.csv", "../data/rf.csv")
    merge_features("../../features/best_featureset_sofar/purchase_features.csv", "../data/pf.csv", "../data/purchase_features.csv")
    merge_features("../../features/best_featureset_sofar/redeem_features.csv", "../data/rf.csv", "../data/redeem_features.csv")



if __name__ == '__main__':
    main()







