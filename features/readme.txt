所有线上线下的跑分数据集均以cleaned为准(20150606将cleaned目录下的数据变为没有清洗过的原始数据)

××××××××××
offline ×
××××××××××
train: 20140401~20140731(X_purchase, X_redeem, y_purchase, y_redeem)
test:  20140801~20140831(X_purchase, X_redeem, y_purchase, y_redeem)

×××××××××
online ×
×××××××××
train: 20140501~20140831(X_purchase, X_redeem, y_purchase, y_redeem)
test:  20140901~20140930(X_purchase, X_redeem, y_purchase, y_redeem)

6.6
将cleaned数据转换为not cleaned数据，重新调整offline/online的train/test时间段，重新gbdt调参，得到108.9分

6.7
purchase/redeem与余额宝收益率/shibor的相关性：从全年数据来看，具有一定的相关性，特别是长期的shibor（达到0.7），但是2014.04之后，purchase和redeem趋于平稳，相关性减弱（基本不相关）
分析：认为前期余额宝刚开通，大家警戒性还比较高，会关注收益率的变化来决定申购和赎回，而2014.04之后大家都习惯了使用余额宝，所以对收益率变化也不再那么敏感，加之余额宝利率也不再强劲（7日年化稳定在4多一点点）
purchase：取mfd_daily_yield, mfd_7daily_yield, Interest_3_M
redeem：取mfd_daily_yield，mfd_7daily_yield，Interest_1_M
加上后效果并不好

6.8
isholyday:2014年中需要上班和不需要上班的日子，相关性非常高，基本上不用上班的日子purchase和redeem都处于波谷
用shouldwork代替isweekend特征得分79,效果不好，主要在于purchase的预测值相差太多（6.9发现是201409的特征有误，重新改正后purchase范围正常，重新提交）

6.9
淘宝天猫做活动的影响：发现影响不大，只有2013.11.11的consume_amt非常高
针对土豪/屌丝用户进行分析
要解决角色带入的问题就必须认真分析不同用户的申购/赎回模式
话外音：感觉挺佩服东哥的，他很清楚知道自己想要什么，而且也很focus在上面，这样的人即便会摔倒，但终究会成功，这一点是我需要向他学习的；而现在很多人都是金玉其外，败絮其中，我不想成为这样的人。

6.10
做了两周了，时间过的真快，剩下两周的时间，其实并不宽裕了，要抓紧时间。
昨天对6.8的特征进行修正后重新提交得分116.77,说明这个方向应该是对的，线上与线下的metric也一致，这是件好事
对dayofweek特征进行dummycoding，变成7个特征。
dummy coding之后purchase和redeem的误差平均值都有所下降，特别是redeem，三个指标都下降了，但是purchase相对误差大于0.3的变成了4个，而且sum of squared relative errors和std of relative errors都变大了，
关键是redeem和purchase的特征相互依赖，怕purchase不准会对redeem造成干扰。

6.11
将dayofmonth转化为百分比：sep的预测值看着不好（特别是purchase，高了许多）

6.12
将dayofmonth转换成percent效果不好，将其转回dayofmonth
将purchase的yesterday_redeem变为week1_redeem,week2_redeem,week3_redeem;同样，把redeem的yesterday_purchase变为week1_purchase,week2_purchase,week3_purchase
发现特征生成有误，将dayofmonth percentile再做一版
九月份第二周和第三周的预测结果大致相同，关键是第一周和最后一周
=======================重新整合特征==================================================
自相关特征（根据pearson相关系数）：
purchase（yesterday_p,week1_p,week2_p,week3_p,week4_p,week1_r,week2_r,week3_r）
redeem(yesterday_r,week1_r,week2_r,week3_r,week4_r,week1_p,week2_p,week3_p)
时间特征（将之前的shouldwork拆分）：
拆分shouldwork：MON，TUE，WED，THU，FRI，SAT，SUN，isholiday，istiaoxiu;
dayofmonth_percent;

6.15
重新整合特征效果更差
现在就是不确定dayofmonth percentile和去yesterday，加week1,2,3两个方案的效果不确定，可以重新试一下，之后可以尝试单点预测和基于用户的分析。
单点预测（基于gbdt_20150610版本）：
20140906：20140405与20140531均值
20140907：20140406与20140601均值
20140908：20140407与20140602均值（purchase挺准的，直接没改）
20140901：2014年4月到8月的第一天上班的平均值
20140928：20140504的值

6.16
(1)基于122得分版本，去除purchase的yesterday_redeem，去除redeem的yesterday_purchase
(2)基于122得分版本，增加本阶段比例（ex:工作期第几天转化为百分比，假期第几天转化为百分比）
(3)基于土豪和屌丝的行为模式分析
