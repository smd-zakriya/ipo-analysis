# -*- coding: utf-8 -*-
"""
Equity IPO price Ananlysis
for currrent price on 18-2-2022 closing 
"""
#%%
import pandas as pd
from datetime import datetime as dt


url = 'https://www.business-standard.com/live-market/ipo/recent-ipos-list/page/'

data = []

for i in range(1,10):
    page = i
    url = url+str(page)
    dt = pd.read_html(url, header=0)[0]
    data.append(dt)
    url = url[:-1]
    
frame = pd.concat(data)

frame.columns = ['company', 'ipo_price', 'curr_price', 'lis_date']
frame.reset_index(drop=True, inplace=True)
frame.set_index('company')
frame.ipo_price = frame.ipo_price.astype('float')
frame.lis_date = pd.to_datetime(frame['lis_date'], format="%b %d,%Y")
frame['percentage'] = round(((frame['curr_price']/frame['ipo_price'])*100), 2)

#%%
#profit and loss
high = frame[frame['curr_price'] > frame['ipo_price']]
high = high.sort_values('percentage', ascending=False)
low = frame[frame['curr_price'] < frame['ipo_price']]
low.loc[:,'percentage'] = low['percentage']-100 
low = low.sort_values('percentage', ascending=True)
no_change = frame[frame['curr_price'] == frame['ipo_price']]

#%%
print('High...',len(high))
print('Low...',len(low))
print('No Change...',len(no_change))
print('Total...',len(frame))
print(high.head())
print(low.head())

#%%
#profit analysis
rise_75 = high[high['curr_price'] > high['ipo_price']*75]
rise_50 = high[(high['curr_price'] > high['ipo_price']*50) & (high['curr_price'] < high['ipo_price']*75)]
rise_20 = high[(high['curr_price'] > high['ipo_price']*20) & (high['curr_price'] < high['ipo_price']*50)]
rise_15 = high[(high['curr_price'] > high['ipo_price']*15) & (high['curr_price'] < high['ipo_price']*20)]
rise_10 = high[(high['curr_price'] > high['ipo_price']*10) & (high['curr_price'] < high['ipo_price']*15)]
rise_5 = high[(high['curr_price'] > high['ipo_price']*5) & (high['curr_price'] < high['ipo_price']*10)]
rise_2 = high[(high['curr_price'] > high['ipo_price']*2) & (high['curr_price'] < high['ipo_price']*5)]
rise_1 = high[high['curr_price'] < high['ipo_price']*2]

profit_gp = [rise_75,rise_50, rise_20, rise_15, rise_10, rise_5, rise_2, rise_1]

#prices rise above ipo price summary
rise_summary = pd.Series({'above_7500': len(rise_75),
                             'above_5000': len(rise_50),
                             'above_2000': len(rise_20),
                             'above_1500': len(rise_15),
                             'above_1000': len(rise_10),
                             'above_500': len(rise_5),
                             'above_200': len(rise_2),
                             'above_100': len(rise_1)})

#loss analysis
fall_5 = low[low['curr_price'] < low['ipo_price']*0.05]
fall_10 = low[(low['curr_price'] < low['ipo_price']*0.1) & (low['curr_price'] > low['ipo_price']*0.05)]
fall_20 = low[(low['curr_price'] < low['ipo_price']*0.2) & (low['curr_price'] > low['ipo_price']*0.1)]
fall_50 = low[(low['curr_price'] < low['ipo_price']*0.5) & (low['curr_price'] > low['ipo_price']*0.2)]
fall_75 = low[(low['curr_price'] < low['ipo_price']*0.75) & (low['curr_price'] > low['ipo_price']*0.5)]
fall_100 = low[low['curr_price'] > low['ipo_price']*0.75]

loss_gp = [fall_5, fall_10, fall_20, fall_50, fall_75, fall_100]

# prises fall below ipo price summary
fall_summary = pd.Series({'below_100': len(fall_100),
                          'below_75': len(fall_75),
                          'below_50': len(fall_50),
                          'below_20': len(fall_20),
                          'below_10': len(fall_10),
                          'below_5': len(fall_5)})

unchanged = pd.Series({'unchanged': len(no_change)})
#overall summary
summary = pd.concat([rise_summary, unchanged, fall_summary], axis=0)
print(summary)

#%%
#plotting --profit--top 25
high_plot = high.iloc[:25, :3]
high_plot.columns = ['Company', 'IPO Price', 'Latest Price']
high_plot.set_index('Company', inplace=True)
high_plot.plot(kind='bar', title="Top 25 performing IPO's of last 3 years (by SMD Zakriya)",
               xlabel='Comapny', ylabel=' Stock Price')

#plotting --loss
low_plot = low.iloc[:25, :3]
low_plot.columns = ['Company', 'IPO Price', 'Latest Price']
low_plot.set_index('Company', inplace=True)
low_plot.plot(kind='bar', title="Top 25 blow out IPO's of last 3 years (by SMD Zakriya)",
               xlabel='Comapny', ylabel=' Stock Price')

#%%
#Exporting data to excel
high.to_excel('profit_ipos.xlsx')
low.to_excel('loss_ipos.xlsx')
summary.to_excel('summary.xlsx')
print('.......done.........')