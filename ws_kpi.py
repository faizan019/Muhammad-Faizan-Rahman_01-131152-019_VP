#!/usr/bin/env python
# coding: utf-8

# In[2]:


import arrow
import pandas as pd
import json
import google.auth
import google.auth
import logging
from string import Template
from meteostat import Daily
from google.cloud import bigquery
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')
from kpi_class import kpi
def kpi_function(kwargs):
    """ This function actually reads data from the source table and perform operations on it and then
        sends back the resultant logs to the destination table in Bigquery.
        Parameters
        ----------
        start_time: timestamp
        It the time from which data will start
        end_time: timestamp
        It the end of the data
        project: GCP project id
        dataset_src: Bigquery source dataset
        location: Project location
        dataset_dest: Bigquery destination dataset
        table_src: Bigquery source table
        table_dest: Bigquery destination table
        Returns
        -------
        This function doesn't return anything
        -------
    """
    start_time = kwargs['start_time']
    end_time = kwargs['end_time']
    project = kwargs['project']
    client_id = kwargs['client_id']
    device_id = kwargs['device_id']
    dataset_src = kwargs['dataset_src']
    dataset_dest = kwargs['dataset_dest']
    table_src = kwargs['table_src']
    table_dest = kwargs['table_dest']
    location = kwargs['location']
    config = kwargs['config']
    def station_data(station_id, start, end):
        data = Daily(station_id, start, end)
        data = data.fetch()
        data.reset_index(inplace=True)
        data = data[['time', 'tavg', 'tmin', 'tmax']]
        #     print(data)
        return data
    def costic(df):
        alias_a = df['tmin']
        alias_b = df['tmax']

        if 15 > alias_b:
            return 15 - (alias_a + alias_b) / 2
        elif 15 <= alias_a:
            return 0
        else:
            return (15 - alias_a) * (0.08 + 0.42 * (15 - alias_a) / (alias_b - alias_a))

    current_time = arrow.utcnow().floor('day')
    # if end_time <= current_time:
    output = config
    rules = pd.DataFrame(output['rules'])
    rules.index = rules.index.astype(int)
    rules.sort_index(inplace=True)
    rules = rules[['kpi_name',
                   'alias_a',
                   'alias_b',
                   'alias_c',
                   'alias_d',
                   'alias_e',
                   'alias_f',
                   'equation_1',
                   'equation_2',
                   'aggregation',
                   'start_time',
                   'end_time',
                   'mute_logs']].copy()
    rules = rules.where(pd.notnull(rules), None)
    settings = output['settings']['mute_rules']
    station_id = output['settings']['station_id']
    country = output['settings']['country']
    state = output['settings']['state']
    df = rules
    # create an empty dataframe
    logs = pd.DataFrame()
    # get access to bigqyery
    # credentials, project_id = google.auth.default()
    # client = bigquery.Client(credentials=credentials)
    if settings is False:
        data_rd = pd.read_csv('main_data.csv')
        data_rd['time'] = pd.to_datetime(data_rd['time_local'])
        if data_rd.shape[0] > 0:
            left_table = data_rd.drop(['alias','value','time_local'],axis=1)
            left_table = left_table.groupby("time").min().reset_index()
            sub_df = data_rd[['time','alias','value']].copy()
            sub_df['value'] = pd.to_numeric(sub_df['value'])
            right_table = pd.pivot_table(sub_df,index='time',columns='alias',values='value').reset_index()
            data_rd = pd.merge(left_table,right_table,on='time', how='outer')
        if data_rd.shape[0] > 0:
            min_time = data_rd.time.min()
            max_time = data_rd.time.max()
            if station_id is not None:
                meteo_data = station_data(station_id, min_time, max_time)
                # print(meteo_data)
                data_rd['costic_HDD_15C'] = meteo_data.apply(costic, axis=1)
                data_rd = data_rd.merge(meteo_data, on='time', how='left')
                data_rd[['tavg', 'tmax', 'tmin']] = data_rd[['tavg', 'tmax', 'tmin']].astype('float')
                print(data_rd.head())
                data_rd.to_csv("file_name.csv", index=False)
            for i in range(df.shape[0]):
                if df.iloc[i]['kpi_name'] == 'costic_HDD_15C':
                    obj = kpi(df.iloc[i], data_rd, country, state, logs)
                    dff = obj.return_log()
                    logs = pd.concat([logs, dff], axis=0)
                    if df.iloc[i]['mute_logs']:
                        aliases_list = df.iloc[i]['mute_logs'].split(',')
                        for alias in aliases_list:
                            logs = logs[~logs.aliases.str.contains(alias.strip())]
        else:
            print(f"Data is not available from {start_time} to {end_time}")
        if logs.shape[0]>0:
            logs['time'] = logs['time'].dt.date
            logs.rename(columns={"time":"date"},inplace=True)
            logs['client_id'] = client_id
            logs['device_id'] = device_id
            logs['date'] = logs['date'].astype(str)
            print(tabulate(logs[['date','value']]))
            # load the logs dataframe to destination table in the bigquery
            # table = client.get_table(f"{project}.{dataset_dest}.{table_dest}")
        else:
            print('no logs saved')
    else:
        print("All rules are muted")








