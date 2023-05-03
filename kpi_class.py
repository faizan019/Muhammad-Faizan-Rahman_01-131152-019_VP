#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import pandas as pd
import numpy as np
import regex as re
import holidays
import arrow
from datetime import time
from functools import reduce
class kpi():
    def __init__(self, rule, batch, country, state, logs):
        if logs.shape[0] > 0:
            logs = logs.pivot_table(index='time', columns='kpi_name', values='value').reset_index()
            batch = batch.merge(logs, on='time', how='left')
        self.country = country
        self.state = state
        # get subset of data, min-time and max-time for the given start and end time
        batch, batch_min_time, batch_max_time = self.__batch_subset(batch, rule['start_time'], rule['end_time'])
        # indices of the rule dataframe
        alias_cols = rule.index
        subs = 'alias'
        # get columns of rule book that alias in their names
        self.__res = [alias_col for alias_col in alias_cols if subs in alias_col]
        self.__rule = rule
        # default logs columns
        log_columns = ['kpi_name', 'time', 'aliases', 'value', 'aggregation']
        log_columns.extend(iter(self.__res))
        # create empty dataframe for the logs
        self.__df_logs = pd.DataFrame(columns=['kpi_name', 'time', 'aliases', 'value', 'aggregation'])
        aliases = []
        # get a list of aliases for the given targets in the rule book and append that lists
        # in the aliases list
        for i in self.__res:
            if rule[i] is not None:
                aliases.append(self.__alias_substrings(batch, [rule[i]], col_name='alias'))
        # in case aliases list length is 1
        # create logs for only one target (alias_a)
        if len(aliases) == 1:
            for alias in aliases[0]:
                # get a dataframe for each alias
                df = self.alias_dataframe(data_rd=batch, aliases=alias)
                # apply the equation that is given in the rule book (equation_1)
                df = self.apply_equation(self, df, equation=rule['equation_1'], temp=True)
                # Aggregate the data after applying equation_1
                df = self.apply_aggregation(self, df, aggregation=rule['aggregation'], kpi=rule['kpi_name'])
                # In case equation_2 is given then apply it after aggregation
                if rule['equation_2'] is not None:
                    df = self.apply_equation(self, df, equation=rule['equation_2'])
                df1 = self.__logs_data(df, rule, [alias])
                self.__df_logs = pd.concat([self.__df_logs, df1], axis=0)
        else:
            alias_pair = self.__alias_pairs(self, rule, aliases)
            for pair in alias_pair:
                if len(pair) != 0:
                    df = self.alias_pairs_dataframe(self, data_rd=batch, aliases=pair)
                    df = self.apply_equation(self, df, equation=rule['equation_1'], temp=True)
                    df = self.apply_aggregation(self, df, aggregation=rule['aggregation'], kpi=rule['kpi_name'])
                    # In case equation_2 is given then apply it after aggregation
                    if rule['equation_2'] is not None:
                        df = self.apply_equation(self, df, equation=rule['equation_2'])
                    df1 = self.__logs_data(df, rule, pair)
                    self.__df_logs = pd.concat([self.__df_logs, df1], axis=0)
    @staticmethod
    def __logs_data(df=None, rule=None, alias_list=None):
        """ Gets resultant dataframe and rules for each kpi and creates logs
            in the form of a dataframe.
        Parameters
        ----------
        df: dataframe
        Resultant dataframe for each kpi
        rule:dataframe
        Its the config file
        tgt_alias:string
        Name of the target alias
        ref_alias: string
        Name of the reference alias
        """
        df1 = pd.DataFrame()
        if len(alias_list) == 1:
            logs_alias = alias_list[0]
        else:
            logs_alias = ",".join(alias_list)
        new_row = {'kpi_name': rule['kpi_name'],
                   'time': df['time'],
                   'aliases': logs_alias,
                   'value': df['value'],
                   'equation_1': rule['equation_1'],
                   'equation_2': rule['equation_2'],
                   'aggregation': rule['aggregation'],
                   }
        df1 = pd.DataFrame(new_row)
        return df1
    @staticmethod
    def country_holidays(df, country, state=None):
        """
        This function returns a list of public holidays for a region/state in country. In case state is not given
         then returns holidays list for that given country.
        """
        df['holiday'] = df['time'].apply(lambda x: 1 if ((x.date() in (holidays.country_holidays(country, subdiv=state)
                                    [str(x.to_period('M').start_time):str(x.to_period('M').end_time)]))
                                                         | (x.dayofweek == 6)) else 0)
        df['working_days'] = df['time'].apply(lambda x:
                                              np.busday_count(arrow.get(x).floor('month').date(),
                                                              arrow.get(x).ceil('month').date(), weekmask='1111110',
                                                              holidays=(
                                                                  holidays.country_holidays(country, subdiv=state)[
                                                                  str(x.to_period('M').start_time):str(
                                                                      x.to_period('M').end_time)])) + 1)
        return df
    @staticmethod
    def apply_equation(self, df=None, equation=None, temp=None):
        def func(x):
            y = eval(equation)
            return y
        if df.shape[0] > 0:
            if equation is not None:
                for col in self.__res:
                    if col in equation:
                        col_name = f"x['{col}']"
                        equation = equation.replace(col, col_name)
                if 'value' in equation:
                    equation = equation.replace('value', "x['value']")
                # time and date base conditions
                if re.search(r'\bday\b', equation):
                    df['day'] = df.time.dt.dayofweek
                    equation = equation.replace('day', 'x["day"]')
                if re.search(r'\bdate\b', equation):
                    df['date'] = df.time.dt.date
                    equation = equation.replace('date', 'str(x["date"])')
                if re.search(r'\btime\b', equation):
                    df['time'] = df.time.apply(lambda x: x.strftime('%H:%M'))
                    equation = equation.replace('time', 'str(x["time"])')
                if re.search(r'\bhour\b', equation):
                    df['hour'] = df.time.dt.hour
                    equation = equation.replace('hour', 'x["hour"]')
                if re.search(r'\bminute\b', equation):
                    df['minute'] = df.time.dt.minute
                    equation = equation.replace('minute', 'x["minute"]')
                if re.search(r"\bmonth\b", equation):
                    df['month'] = df.time.dt.month
                    equation = equation.replace('month', 'x["month"]')
                if re.search(r'\bholiday\b', equation):
                    df = self.country_holidays(df, self.country, state=self.state)
                    equation = equation.replace('holiday', 'x["holiday"]')
                if re.search(r"\bworking_days\b", equation):
                    equation = equation.replace('working_days', 'x["working_days"]')
                df['value'] = df.apply(func, axis=1)
            else:
                df['value'] = df['alias_a']
        return df
    @staticmethod
    def apply_aggregation(self, df=None, aggregation='mean', kpi=None):
        if df.shape[0] > 0:
            if aggregation == 'perc':
                aggregation = 'mean'
            df.set_index('time', inplace=True)
            x = f"df.resample('D').{aggregation}()"
            df = eval(x)
            df.reset_index(inplace=True)
            df['kpi'] = kpi
        df.loc[df["value"] == True, "value"] = 1
        df.loc[df["value"] == False, "value"] = 0
        return df
    @staticmethod
    def __alias_substrings(df, in_list, col_name='alias'):
        """ This function returns a list of aliases for a given reference in the
            the config file.
        Parameters
        ----------
        df: dataframe
        It's the source dataframe
        in_list: list
        It's the list of given aliases in the config file
        col_name: string
        It's the column name in the source dataframe
        Returns
        -------
        filtered_aliases: list
        This list contains the aliases that are filtered out
        """
        groups = in_list
        substrings = []
        filtered_aliases = []
        # Creating list of substrings
        for group_id in groups:
            print("group_id ==> ", group_id)
            print("group_id data type ==> ", type(group_id))
            substrings.append(group_id.split('_'))
        unique_aliases = df.columns
        # print(unique_aliases)
        # Removing None from the list of unique aliases
        unique_aliases = list(filter(None, unique_aliases))
        # Filter the aliases that are to be used for the KPI
        for alias in unique_aliases:
            for sub in substrings:
                if all(a in alias for a in sub):
                    filtered_aliases.append(alias)
        return filtered_aliases
    @staticmethod
    def __batch_subset(batch, start_time, end_time):
        """Gets a dataframe and a specific duration, where it takes a subset
        of dataframe that falls in the start and end times.
        Parameters
        ----------
        batch: dataframe
        The source dataframe
        start_time: timestamp
        This will be the start or minimum time of the dataframe
        end_time: timestamp
        This be the end or maximum time of the dataframe
        Returns
        ------
        batch: dataframe
        This is resultant dataframe between the start and end times
        batch_min_time: timestamp
        The minimum time of the dataframe
        batch_max_time: timestamp
        The maximum time of the dataframe
        """
        # in case start time is given
        if start_time is not None:
            # start_time = str(start_time)
            # split the time(string) in hour,min and secs
            hour = start_time.split(':')[0]
            minute = start_time.split(':')[1]
            second = start_time.split(':')[2]
            print(f'start_time {time(int(hour), int(minute), int(second))}')
            # filter dataframe having time  greater or equal  to start time
            batch = batch.loc[batch['time'].dt.time >= time(int(hour), int(minute), int(second))]
        # in case end time is given
        if end_time is not None:
            # end_time = str(end_time)
            # split the time(string) in hour,min and secs
            hour = end_time.split(':')[0]
            minute = end_time.split(':')[1]
            second = end_time.split(':')[2]
            print(f"end_time {time(int(hour), int(minute), int(second))}")
            # filter dataframe having time  smaller than the  end time
            batch = batch.loc[batch['time'].dt.time < time(int(hour), int(minute), int(second))]
        # get miminium and maximum time of the dataframe
        batch_min_time = batch.time.min()
        batch_max_time = batch.time.max()
        return batch, batch_min_time, batch_max_time
    @staticmethod
    def alias_pairs_dataframe(self, data_rd=None, aliases=None):
        df_master = pd.DataFrame()
        res = [index for index, val in enumerate(aliases)]
        alias_cols = aliases.copy()
        alias_cols.append('time')
        cols = [val for index, val in enumerate(self.__res) if index in res]
        cols.append('time')
        df = data_rd[alias_cols].copy()
        df.columns = cols
        if df.shape[0] > 0:
            df_master = df
        return df_master
    @staticmethod
    def alias_dataframe(data_rd=None, aliases=None):
        df_master = pd.DataFrame()
        df = data_rd[['time', aliases]].copy()
        df.rename(columns={aliases: 'alias_a'}, inplace=True)
        df_master = df
        return df_master
    @staticmethod
    def __alias_pairs(self, rule, aliases):
        self.__index = [index for index, val in enumerate(aliases)]
        col_names = self.__res
        col_names = [val for index, val in enumerate(col_names) if index in self.__index]
        null_list_index = [index for index, val in enumerate(aliases) if len(val) == 0]
        non_null_dfs_list = []
        null_dfs_list = []
        for i in range(len(aliases)):
            non_null_alias_df = pd.DataFrame(columns=['alias', 'keys'])
            null_alias_df = pd.DataFrame(columns=['alias', 'keys'])
            if len(aliases[i]) > 0:
                for alias in aliases[i]:
                    keys = alias.split("_")
                    for ele in rule[col_names[i]].strip().split('_'):
                        keys.remove(ele)
                    if len(keys) == 0:
                        df = pd.DataFrame([[alias, None]], columns=['alias', 'keys'])
                        null_alias_df = pd.concat([null_alias_df, df], axis=0, ignore_index=True)
                    else:
                        key = '_'.join(map(str, keys))
                        df = pd.DataFrame([[alias, key]], columns=['alias', 'keys'])
                        non_null_alias_df = pd.concat([non_null_alias_df, df], axis=0, ignore_index=True)
            if non_null_alias_df.shape[0] > 0:
                non_null_dfs_list.append(non_null_alias_df)
            if null_alias_df.shape[0] > 0:
                null_dfs_list.append(null_alias_df)
        if len(null_dfs_list) == len(col_names):
            nulls_df_merge = reduce(lambda left, right: pd.merge(left, right, how="cross"), null_dfs_list)
            non_nulls_df_merge = pd.DataFrame(columns=['alias', 'keys'])
        else:
            if len(non_null_dfs_list) > 1:
                non_nulls_df_merge = reduce(lambda left, right: pd.merge(left, right, on=["keys"], how="inner"),
                                            non_null_dfs_list)
            elif len(non_null_dfs_list) == 1:
                non_nulls_df_merge = non_null_dfs_list[0]
            else:
                non_nulls_df_merge = pd.DataFrame(columns=['alias', 'keys'])
            if len(null_dfs_list) > 1:
                nulls_df_merge = reduce(lambda left, right: pd.merge(left, right, how="cross"), null_dfs_list)
            elif len(null_dfs_list) == 1:
                nulls_df_merge = null_dfs_list[0]
            else:
                nulls_df_merge = pd.DataFrame(columns=['alias', 'keys'])
        if nulls_df_merge.shape[0] > 0 and non_nulls_df_merge.shape[0] > 0:
            alias_pairs_df = pd.merge(nulls_df_merge, non_nulls_df_merge, how='cross')
        elif nulls_df_merge.shape[0] == 0:
            alias_pairs_df = non_nulls_df_merge
        elif non_nulls_df_merge.shape[0] == 0:
            alias_pairs_df = nulls_df_merge
        subs = 'keys'
        keys_cols = [col for col in alias_pairs_df if subs in col]
        alias_pairs_df = alias_pairs_df.drop(keys_cols, axis=1)
        if alias_pairs_df.shape[1] == len(col_names):
            alias_pairs = alias_pairs_df.values.tolist()
        else:
            alias_pairs = []
        return alias_pairs
    def return_log(self):
        return self.__df_logs


# In[ ]:




