#!/usr/bin/env python
# coding: utf-8

# ## Data used: http://ergast.com/mrd/

# ##### Formule 1 dataset

# In[2]:


# !pip install streamlit==1.13.0


# In[3]:


# !pip install mymodel


# In[4]:


import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st 


# In[5]:


pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', None)


# In[6]:


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


# In[7]:


df_seasons_races = pd.json_normalize(seasons_races, 
    record_path=['Results'], 
    meta=['season', 'round', 'raceName', 'date', 'time', ['Circuit', 'circuitName'], ['Circuit', 'Location', 'locality'], ['Circuit', 'Location', 'country']]
)

df_seasons_races.head(5)


# In[8]:


df_seasons_races.shape


# In[9]:


df_seasons_races.dtypes


# In[10]:


df_seasons_races.info()


# In[11]:


df_seasons_races[['season', 'round']] = df_seasons_races[['season', 'round']].astype(int)
df_seasons_races[['points']] = df_seasons_races[['points']].astype(float)


# In[12]:


df_seasons_races['totalPointsDriver'] = df_seasons_races.groupby(by=['season','Driver.driverId'])['points'].transform('cumsum')
df_seasons_races['totalPointsConstructor'] = df_seasons_races.groupby(by=['season','Constructor.constructorId'])['points'].transform('cumsum')


# In[13]:


df_2021 = df_seasons_races[df_seasons_races['season'] == 2021]


# In[41]:


fig1 = px.line(df_2021, x="round", y="totalPointsDriver", color='Driver.familyName', 
              title="Gecumuleerd aantal punten per coureur per race in seizoen 2021", range_y=[0,450])

# Create the buttons
dropdown_buttons = [
{'label': "ALL", 'method': "update", 'args': [{"visible": [True]}, {"title": "Gecumuleerd aantal punten per coureur per race in seizoen 2021"}]},
{'label': "Hamilton", 'method': "update", 'args': [{"visible": [True, False, False, False, False, False, False, False, False, False,
                                                                 False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Hamilton per race in seizoen 2021"}]},
{'label': "Verstappen", 'method': "update", 'args': [{"visible": [False, True, False, False, False, False, False, False, False, False,
                                                               False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Verstappen per race in seizoen 2021"}]},
{'label': "Bottas", 'method': "update", 'args': [{"visible": [False, False, True, False, False, False, False, False, False, False,
                                                             False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Bottas per race in seizoen 2021"}]},
{'label': "Norris", 'method': "update", 'args': [{"visible": [False, False, False, True, False, False, False, False, False, False,
                                                            False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Norris per race in seizoen 2021"}]},
{'label': "Pérez", 'method': "update", 'args': [{"visible": [False, False, False, False, True, False, False, False, False, False,
                                                            False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Pérez per race in seizoen 2021"}]},
{'label': "Leclerc", 'method': "update", 'args': [{"visible": [False, False, False, False, False, True, False, False, False, False,
                                                             False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Leclerc per race in seizoen 2021"}]},
{'label': "Ricciardo", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, True, False, False, False,
                                                              False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Ricciardo per race in seizoen 2021"}]},
{'label': "Sainz", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, True, False, False,
                                                                False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Sainz per race in seizoen 2021"}]},
{'label': "Tsunoda", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, True, False,
                                                            False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Tsunoda per race in seizoen 2021"}]},
{'label': "Stroll", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, True,
                                                             False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Stroll per race in seizoen 2021"}]},
{'label': "Räikkönen", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                            True, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Räikkönen per race in seizoen 2021"}]},
{'label': "Giovinazzi", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, True, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Giovinazzi per race in seizoen 2021"}]},
{'label': "Ocon", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, False, True, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Ocon per race in seizoen 2021"}]},
{'label': "Russel", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                              False, False, False, True, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Russel per race in seizoen 2021"}]},
{'label': "Vettel", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, False, False, False, True, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Vettel per race in seizoen 2021"}]},
{'label': "Schumacher", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                                False, False, False, False, False, True, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Schumacher per race in seizoen 2021"}]},
{'label': "Gasly", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, False, False, False, False, False, True, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Gasly per race in seizoen 2021"}]},
{'label': "Latifi", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                                 False, False, False, False, False, False, False, True, False, False, False]}, {"title": "Gecumuleerd aantal punten Latifi per race in seizoen 2021"}]},
{'label': "Alonso", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                              False, False, False, False, False, False, False, False, True, False, False]}, {"title": "Gecumuleerd aantal punten Alonso per race in seizoen 2021"}]},
{'label': "Mazepin", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, False, False, False, False, False, False, False, False, True, False]}, {"title": "Gecumuleerd aantal punten Mazepin per race in seizoen 2021"}]},
{'label': "Kubica", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, False, False, False, False, False, False, False, False, False, True]}, {"title": "Gecumuleerd aantal punten Kubica per race in seizoen 2021"}]},
]

fig1.update_layout({'updatemenus': [
        {'active': 0, 'buttons': dropdown_buttons}
        ]})
fig1.update_xaxes(type='category', title={'text': 'Race'})
fig1.update_yaxes(title={'text': 'Gecumuleerd aantal punten'})
fig1.update_layout(legend_title_text='Coureur')
fig1.show()


# In[40]:


fig2 = px.line(df_2021, x="round", y="totalPointsConstructor", color='Constructor.name', 
              title="Gecumuleerd aantal punten per constructeur per race in seizoen 2021", range_y=[0,650])

# Create the buttons
dropdown_buttons = [
{'label': "ALL", 'method': "update", 'args': [{"visible": [True, True, True]}, {"title": "Gecumuleerd aantal punten per constructeur per race in seizoen 2021"}]},
{'label': "Mercedes", 'method': "update", 'args': [{"visible": [True, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Mercedes per race in seizoen 2021"}]},
{'label': "Red Bull", 'method': "update", 'args': [{"visible": [False, True, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Red Bull per race in seizoen 2021"}]},
{'label': "McLaren", 'method': "update", 'args': [{"visible": [False, False, True, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten McLaren per race in seizoen 2021"}]},
{'label': "Ferrari", 'method': "update", 'args': [{"visible": [False, False, False, True, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Ferrari per race in seizoen 2021"}]},
{'label': "AlphaTauri", 'method': "update", 'args': [{"visible": [False, False, False, False, True, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten AlphaTauri per race in seizoen 2021"}]},
{'label': "Aston Martin", 'method': "update", 'args': [{"visible": [False, False, False, False, False, True, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Aston Martin per race in seizoen 2021"}]},
{'label': "Alfa Romeo", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, True, False, False, False]}, {"title": "Gecumuleerd aantal punten Alfa Romeo per race in seizoen 2021"}]},
{'label': "Alpine F1 Team", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, True, False, False]}, {"title": "Gecumuleerd aantal punten Alpine F1 Team per race in seizoen 2021"}]},
{'label': "Williams", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, True, False]}, {"title": "Gecumuleerd aantal punten Williams per race in seizoen 2021"}]},
{'label': "Haas F1 Team", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, True]}, {"title": "Gecumuleerd aantal punten Haas F1 Team per race in seizoen 2021"}]},
]

# Update the figure to add dropdown menu
fig2.update_layout({'updatemenus': [
        {'active': 0, 'buttons': dropdown_buttons}
        ]})

fig2.update_xaxes(type='category', title={'text': 'Race'})
fig2.update_yaxes(title={'text': 'Gecumuleerd aantal punten'})
fig2.update_layout(legend_title_text='Constructeur')
fig2.show()


# In[42]:


col1, col2 = st.columns([3, 1])
col1.write(fig1)
col1.write(fig2)

