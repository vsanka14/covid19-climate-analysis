
# coding: utf-8

# In[205]:


import pandas as pd
import os 
import json
import datetime 

directory = '../data'
all_dfs = {}
aggregation_functions = {'Confirmed': 'sum', 'Deaths': 'sum', 'Recovered': 'sum', 'Province_State': 'first'}
for filename in os.listdir(directory):
    if not filename.startswith('.'):            
        df = pd.read_csv(f'{directory}/{filename}')
        cols = df.columns.values
        for i in range(len(cols)):
            if cols[i] == 'Province/State':
                cols[i] = 'Province_State'
            if cols[i] == 'Country/Region':
                cols[i] = 'Country_Region'
        df.columns = cols
        df = df.loc[df['Country_Region'] == 'US']
        df_new = df.groupby(df['Province_State']).aggregate(aggregation_functions)
        all_dfs[filename.replace('.csv', '')] = df_new


# In[207]:


states = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
states_data = {}
for state in states:
    states_data[state] = []
for date in all_dfs:
    df = all_dfs[date]
    for state in states:
        state_dict = {}
        state_df = df.loc[df['Province_State']==state]
        state_dict['date'] = date
        state_dict['confirmed'] = 0
        if len(list(state_df['Confirmed'])) > 0:
            state_dict['confirmed'] = list(state_df['Confirmed'])[0]
        states_data[state].append(state_dict)


# In[208]:


states_df = {}
for state in states_data:
    df = pd.DataFrame(states_data[state])
    states_df[state] = df


# In[209]:


def calc_avg(weather_data, date, field):
    tod = datetime.datetime.strptime(date, '%m-%d-%Y')
    no_of_days = 14
    d = datetime.timedelta(days = no_of_days)
    sum = 0
    while(no_of_days > 0):
        a = (tod - d).strftime('%m-%d-%Y')
        try:
            sum +=  int(weather_data[a][field])
        except:
            print(a)
        no_of_days -= 1
    return sum/14

def add_temp_and_humidity(state):
    weather_data = None
    with open(f'../weather_data/{state}.json') as f:
      weather_data = json.load(f)
    states_df[state]['max_temp'] = states_df[state]['date'].map(lambda x: calc_avg(weather_data, x, 0))
    states_df[state]['humidity'] = states_df[state]['date'].map(lambda x: calc_avg(weather_data, x, 1))


# In[210]:


add_temp_and_humidity('Arizona')


# In[211]:


states_df['Arizona']


# In[138]:


str = '03-24-2020'
int(str.split('-')[1])


# In[142]:


str = 'abc'
str.replace('z', '')


# In[167]:


import datetime 
tod = datetime.datetime.strptime('03-10-2020' , '%m-%d-%Y')
d = datetime.timedelta(days = 14)
a = tod - d
print(a.strftime('%m-%d-%Y'))


# In[161]:


datetime.datetime.strptime('2012-02-10' , '%Y-%m-%d')

