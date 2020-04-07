import pandas as pd
import os 
import json
import datetime 
import numpy as np
from statsmodels.regression.linear_model import OLS
import seaborn as sns

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


states_df = {}
for state in states_data:
    df = pd.DataFrame(states_data[state])
    states_df[state] = {}
    states_df[state]['data'] = df


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
            print('exception: ', weather_data[a], a)
        no_of_days -= 1
    return sum/14

def add_temp_and_humidity(state):
    weather_data = None
    with open(f'../weather_data/{state}.json') as f:
      weather_data = json.load(f)
    states_df[state]['data']['max_temp'] = states_df[state]['data']['date'].map(lambda x: calc_avg(weather_data, x, 'maxTemp'))
    states_df[state]['data']['humidity'] = states_df[state]['data']['date'].map(lambda x: calc_avg(weather_data, x, 'maxHumidity'))

def add_new_cases(state):
    l=[]
    for x,y in enumerate(states_df[state]['data']['confirmed']):
        if x == 0: 
           l.append(y)
        else : 
           l.append(y-l[x-1])
    states_df[state]['data']['new_cases'] = l 


def create_scaled_df(df):
    y = np.log(df.iloc[:, -1]) #take log of number of cases
    y.name = 'Infected cases' 
    y = y.to_frame()
    temp = 60
    humid = 75
    x = df[['max_temp', 'humidity']].sub([temp, humid])  
    x.columns = ['Temp - 60F', 'Humidity - 75%']

    scaled_df = pd.merge(left = x, right = y, left_on= x.index, right_on= y.index)
    scaled_df = scaled_df.replace([np.inf, -np.inf], 0)
    return scaled_df


def prepare_state_df(state):
    states_df[state]['data']['datetime'] = states_df[state]['data']['date'].map(lambda x: datetime.datetime.strptime(x, '%m-%d-%Y'))
    states_df[state]['data'] = states_df[state]['data'].sort_values(by='datetime')
    add_temp_and_humidity(state)
    add_new_cases(state)
    state_df = create_scaled_df(states_df[state]['data'])
    return state_df


for state in states_data:
    scaled_df = prepare_state_df(state)
    target = scaled_df.loc[:,'Infected cases']
    features = scaled_df.loc[:, 'Temp - 60F':'Humidity - 75%']
    result = OLS(target, features, hasconst=False).fit()
    states_df[state]['scaled_df'] = scaled_df
    states_df[state]['result'] = result
    states_df[state]['max_infected'] = scaled_df['Infected cases'].max()

return states_df