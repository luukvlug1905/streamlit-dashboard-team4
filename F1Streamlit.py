#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st 


# In[2]:


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', None)


# In[3]:


seasons = [2021, 2020, 2019, 2018, 2017]

seasons_races = []

for season in seasons:
    
    url = 'https://ergast.com/api/f1/' + str(season) + '.json'
    
    response = requests.get(url)

    if response.status_code != 200:

        print('Error fetching data from source: ' + url)

    else:

        data = response.json()

        for race in data['MRData']['RaceTable']['Races']:
            
            url = 'http://ergast.com/api/f1/' + str(season) + '/' + race['round'] + '/results.json'
            
            response = requests.get(url)

            if response.status_code != 200:

                print('Error fetching data from source: ' + url)

            else:

                data = response.json()

                seasons_races.append(data['MRData']['RaceTable']['Races'][0])

                print('Successfully fetched data from source: ' + url + '.')


# In[4]:


df_seasons_races = pd.json_normalize(seasons_races, 
    record_path=['Results'], 
    meta=['season', 'round', 'raceName', 'date', 'time', ['Circuit', 'circuitName'], ['Circuit', 'Location', 'locality'], ['Circuit', 'Location', 'country']]
)

df_seasons_races.head(5)


# In[5]:


df_seasons_races[['season', 'round']] = df_seasons_races[['season', 'round']].astype(int)
df_seasons_races[['points']] = df_seasons_races[['points']].astype(float)


# In[6]:


df_seasons_races['totalPointsDriver'] = df_seasons_races.groupby(by=['season','Driver.driverId'])['points'].transform('cumsum')
df_seasons_races['totalPointsConstructor'] = df_seasons_races.groupby(by=['season','Constructor.constructorId'])['points'].transform('cumsum')


# In[7]:


df_2021 = df_seasons_races[df_seasons_races['season'] == 2021]


# In[8]:


fig123 = px.line(df_2021, x="round", y="totalPointsDriver", color='Driver.driverId')
fig123.update_xaxes(type='category')
fig123.show()


# In[9]:


st.write(fig123)


# In[ ]:




