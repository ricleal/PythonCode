import pandas as pd
from datetime import timedelta, datetime

day_of_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
               3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

df = pd.read_csv('aws738.csv', sep='\t')


df['Arrival'] = df['Arrival'].str.replace('WEST \(\+1\)', 'GMT+1')


df["Departure"] = pd.to_datetime(df['Date'] + ' ' + df['Departure'])
df["Arrival"] = pd.to_datetime(df['Date'] + ' ' + df['Arrival'])

df["Arrival"] = df["Arrival"] + timedelta(days=1)

df["Date"] = pd.to_datetime(df["Date"])

#df['scheduled_arrival'] = pd.to_datetime( [str(i)[0:10] + ' 8:50 AM GMT+1' for i in df['Arrival']])
df['scheduled_arrival'] = pd.Series(
    [str(i)[0:10] + ' 8:50 AM GMT+1' for i in df['Date']])
df['scheduled_arrival'] = pd.to_datetime(df.scheduled_arrival)

#df['scheduled_departure'] = pd.Series([str(i)[0:10] + ' 8:45 PM EST' for i in df['Departure']])
df['scheduled_departure'] = pd.to_datetime(
    [str(i)[0:10] + ' 8:45 PM EST' for i in df['Date']])
df['scheduled_departure'] = pd.to_datetime(df.scheduled_departure)

df[["Departure", 'scheduled_departure']]
df = df.drop(df.index[[108, 109]])

df['delay_departure'] = df["Departure"] - df['scheduled_departure']

df['delay_departure'].mean()

index_date = pd.DatetimeIndex(df['Date'])
# index_date.weekday
weekday = df['Date'].dt.dayofweek.map(day_of_week)
#weekday = df['Date'].apply(lambda x: dt.datetime.strftime(x, '%A'))

index_delay = pd.DatetimeIndex(df['delay_departure'])
total_minutes_delay = [
    h * 60 + m for h, m in zip(index_delay.hour, index_delay.minute)]


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set(color_codes=Truue, style="ticks")
sns.distplot(total_minutes_delay)

g = sns.kdeplot(index_date.weekday, np.array(total_minutes_delay),xticks=np.unique(weekday), shade=True)
g.set(xticklabels=day_of_week.values())
g.set(xlim=(0, 6))
plt.xticks(rotation=90) 
plt.show()

# joint plot
with sns.axes_style("white"):
    g = sns.jointplot(index_date.weekday, np.array(
        total_minutes_delay), kind="kde", xlim=(0, 6))
    
    plt.xticks(np.unique(index_date.weekday), weekday, rotation='vertical')

plt.show()
