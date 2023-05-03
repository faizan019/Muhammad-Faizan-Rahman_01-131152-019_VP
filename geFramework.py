import datetime
import pandas as pd
from functools import reduce
import regex as re
import warnings
import arrow
import json
import os
import requests
import numpy as np
import math
from dotenv import load_dotenv
import io
import requests
from google.cloud import storage
import matplotlib.pyplot as plt
load_dotenv()

# supress warnings to debugging
warnings.filterwarnings("ignore")

# PROJECT_ID = os.environ['PROJECT_ID']
# DEST_DATASET_ID = os.environ['DEST_DATASET_ID']
# DEST_TABLE_ID = os.environ['DEST_TABLE_ID']
SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')
print(SLACK_WEBHOOK)


class geFramework():
    def __init__(self, rule, batch):

        # get subset of data, min-time and max-time for the given start and end time
        # batch = self.__batch_subset(batch, rule['duration_hours'])
        # print(rule)
        if 'missing_values' not in rule['rule_name']:
            batch.fillna(method='ffill', inplace=True)
        # indices of the rule dataframe
        alias_cols = rule.index
        subs = 'alias'
        # get columns of rule book that alias in their names
        self.__res = [
            alias_col for alias_col in alias_cols if subs in alias_col]
        self.__rule = rule

        # create empty dataframe for the logs
        self.__df_logs = pd.DataFrame(columns=[
            'rule_name', 'aliases', 'criticality', 'time_local', 'test', 'date_update','qa'])
        aliases = []
        # get a list of aliases for the given targets in the rule book and append that lists
        # in the aliases list

        # in case alias_a is not null
        if rule[self.__res[0]] is not None:

            for i in self.__res:
                if rule[i] is not None and '-' not in rule[i]:
                    # get all aliases for given keywords in config columns
                    aliases.append(self.__alias_substrings(
                        batch, [rule[i]], col_name='alias'))

                # In case minus sign is found to exclude that given alias
                elif rule[i] is not None and '-' in rule[i]:
                    keyword = rule[i].replace('-', '').strip()
                    # get all aliases for given keyword in config columns
                    excluded_aliases = self.__alias_substrings(
                        batch, [keyword], col_name='alias')
                    # get all columns(aliases) of the dataframe
                    unique_aliases = batch.columns.to_list()
                    # drop the given keyword's aliases and time_local from all aliases in dataframe
                    required_aliases = list(
                        set(unique_aliases) - set(excluded_aliases) - set(['time_local']))
                    # append required aliases in the aliases list
                    aliases.append(required_aliases)

            # in case there is only one group of aliases in aliases list
            if len(aliases) == 1:
                # iterate over all group of  alaises
                for alias in aliases[0]:

                    # get a dataframe for each alias
                    df = self.alias_dataframe(self, data_rd=batch, aliases=alias, kpi=rule['rule_name'],
                                              resample_grain=None, daily_resample=None, agg=None, non_negative=None)
                    # in case dataframe is not empty
                    if df.shape[0] > 0:
                        # apply the equation that is given in the rule book (equation_1)
                        df = self.apply_equation_1(
                            self, df, equation=rule['equation_1'], temp=True).reset_index(drop=True)

                        df = self.apply_equation_2(
                            self, df, rule, equation=rule['equation_2'])
                        # create logs
                        df1 = self.__logs_data(df, rule, [alias])
                        self.__df_logs = pd.concat(
                            [self.__df_logs, df1], axis=0)

                    # in case dataframe is empty
                    else:
                        print(f'Data is not available for {alias}')
            # if in case there are multiple aliases groups in aliases list
            else:

                # create a list of different pairs of aliases
                alias_pair = self.__alias_pairs(self, batch, rule, aliases)

                # iterate for all pairs
                for pair in alias_pair:

                    # in case length of a pair is not equal to 0
                    if len(pair) != 0:
                        # get a dataframe for each pair
                        df = self.alias_pairs_dataframe(self, data_rd=batch, aliases=pair, kpi=rule['rule_name'],
                                                        resample_grain=None, daily_resample=None, agg=None,
                                                        non_negative=None)
                        # in case dataframe is not empty
                        if df.shape[0] > 0:
                            # apply the equation that is given in the rule book (equation_1)
                            df = self.apply_equation_1(
                                self, df, equation=rule['equation_1'], temp=True).reset_index(drop=True)

                            df = self.apply_equation_2(
                                self, df, rule, equation=rule['equation_2'])
                            #                     # create logs
                            df1 = self.__logs_data(df, rule, pair)
                            self.__df_logs = pd.concat(
                                [self.__df_logs, df1], axis=0)
                    # in case dataframe is empty
                    else:
                        print(f'Data is not available for {pair}')
        # if in case alias_a is null
        else:
            # get all columns (aliases) of the dataframe except time_local or time
            aliases.append(self.__alias_substrings(
                batch, None, col_name='alias'))
            # iterate for all aliases
            for alias in aliases[0]:
                # get a dataframe for each pair
                df = self.alias_dataframe(self, data_rd=batch, aliases=alias, kpi=rule['rule_name'],
                                          resample_grain=None, daily_resample=None, agg=None, non_negative=None)
                # in case dataframe is not empty
                if df.shape[0] > 0:
                    # apply the equation that is given in the rule book (equation_1)
                    df = self.apply_equation_1(
                        self, df, equation=rule['equation_1'], temp=True).reset_index(drop=True)

                    df = self.apply_equation_2(
                        self, df, rule, equation=rule['equation_2'])
                    #                     # create logs
                    df1 = self.__logs_data(df, rule, [alias])
                    self.__df_logs = pd.concat([self.__df_logs, df1], axis=0)
                # in case dataframe is empty
                else:
                    print(f'Data is not available for {alias}')

    @staticmethod
    def __logs_data(df=None, rule=None, alias_list=None, result=None):
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
        # create an empty dataframe
        df1 = pd.DataFrame()

        # concate all aliases as one string
        if len(alias_list) == 1:
            logs_alias = alias_list[0]
        else:
            logs_alias = ",".join(alias_list)

        # get current utc time (function running time) for date_update
        # current_time = datetime.datetime.utcnow().replace(
        #     second=0, microsecond=0)

        df1 = df[['test', 'time_local']].copy()
        df1['aliases'] = logs_alias
        df1['rule_name'] = rule['rule_name']
        df1['criticality'] = rule['criticality']
        df1['qa'] = rule['qa']

        # if rule.mute_alert is not None:
            # print(logs_alias)
            # print(rule.mute_alert)
        #     for x in rule.mute_alert.split(','):
        #         print(x)
        #         # df1['mute_alert'] = np.where(df1.aliases.str.contains(x), "muted", None)
        #         df1.loc[df1.aliases.str.contains(x),'mute_alert'] = "muted"
        #         df1['mute_alert'] = df1['mute_alert'].fillna(None)
        # else:
        #     df1['mute_alert'] = None
        return df1

    @staticmethod
    def count(df, max_delta):

        try:
            count_true = df['value'].value_counts()[True]
        except:
            count_true = 0

        return count_true

    @staticmethod
    def streak(df):
        """This function calculates delta for only true values, in case
        this calculated delta is greater or equal to the max_delta then
        test will fail otherwise pass.
        Parameters
        ----------
        df : dataframe
        Dataframe after applying equation
        rule: dataframe
        Each row of the config file as a dataframe
        Returns
        -------
        df: dataframe
        delta: float
        """

        # set True value to 1 and False to 0
        df.loc[df["value"] == True, "value"] = 1
        df.loc[df["value"] == False, "value"] = 0
        # Check that original values are not equal to shifted values
        df['expected_streak'] = df.value.ne(df.value.shift())
        # get timelocal for the start of streak
        df['streak_time'] = df.loc[df.expected_streak == True]['time_local']
        # convert streak start time to datetime
        df['streak_time'] = pd.to_datetime(df['streak_time'])
        # converte time_local to datetime
        df['time_local'] = pd.to_datetime(df['time_local'])
        # fill null values from previous values by using forward filling
        df = df.fillna(method='ffill')
        # calculate delta in minutes
        df['delta'] = (df['time_local'] - df['streak_time']
                       ).dt.total_seconds() / 60

        return df

    @staticmethod
    def apply_equation_1(self, df=None, equation=None, temp=None):
        """ This function basically takes a dataframe and an equation
        and then tries to apply this equation and results in the form of boolean.
        Parameters
        ----------
        df: Dataframe
        A Dataframe for an aliases or a pair of aliases
        equation: String
        This string has a set of instruction
        Returns
        -------
        df: Dataframe
        """

        def func(x):
            y = eval(equation)
            return y

        if df.shape[0] > 0:
            df['time_local'] = pd.to_datetime(df['time_local'])
            # in case equation is given and not missing_values or constant values
            if equation is not None:
                # iterate for given given alias columns in the config file
                for col in self.__res:
                    # add dataframe with alias column
                    if col in equation:
                        col_name = f"x['{col}']"
                        equation = equation.replace(col, col_name)

                # time and date base conditions
                if 'day' in equation:
                    df['day'] = df.time_local.dt.dayofweek
                    equation = equation.replace('day', 'x["day"]')
                if 'date' in equation:
                    df['date'] = df.time_local.dt.date
                    equation = equation.replace('date', 'str(x["date"])')
                if 'time' in equation:
                    df['time'] = df.time_local.apply(lambda x: x.strftime('%H:%M'))
                    equation = equation.replace('time', 'str(x["time"])')
                if 'hour' in equation:
                    df['hour'] = df.time_local.dt.hour
                    equation = equation.replace('hour', 'x["hour"]')
                if 'minute' in equation:
                    df['minute'] = df.time_local.dt.minute
                    equation = equation.replace('minute', 'x["minute"]')
                if 'month' in equation:
                    df['month'] = df.time_local.dt.month
                    equation = equation.replace('month', 'x["month"]')

                # apply equation
                df['value'] = df.apply(func, axis=1)
            # in case equation is None
            else:
                df['value'] = df['alias_a']

        return df

    @staticmethod
    def apply_equation_2(self, df=None, rule=None, equation=None, kpi=None):
        if df.shape[0] > 0:
            if equation is not None:
                if 'streak' in equation:
                    df = self.streak(df)
                    duration = float(re.findall("[0-9.]+", equation)[0])
                    frac, whole = math.modf(duration)
                    duration = (whole * 60 - 15 if whole != 0 else 0) + (frac * 60)
                    equation = f'(df.delta >={duration}) & (df.value == True)'
                    df['test'] = eval(equation)

                else:
                    aggregation = re.findall('\w+', equation)[0]
                    operator = re.findall("[^a-zA-Z0-9_.,\s\(\)\[\]]+", equation)[0]
                    window = rule['duration_hours']
                    duration = str(window) + 'h'
                    threshold = float(re.findall("[0-9]+", equation)[0])
                    df['time_local'] = pd.to_datetime(df['time_local'])
                    df.set_index('time_local', inplace=True)
                    df['test'] = eval(f"df['value'].rolling('{duration}',min_periods = {window} * 4 ).agg('{aggregation}') {operator} {threshold}")
                    df.reset_index(inplace=True)
            else:
                df.self.streak(df)
                duration = float(rule['duration_hours'])
                frac, whole = math.modf(duration)
                duration = (whole * 60 - 15 if whole != 0 else 0) + (frac * 60)
                equation = f'(df.delta >={duration}) & (df.value == True)'
                df['test'] = eval(equation)

            #             display(df)
            df = df.loc[df.test == True]
            df.test = 'fail'

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

        if in_list is not None:
            filtered_aliases = []
            substrings = []

            # Creating list of substrings
            for group_id in groups:
                # print(group_id)
                substrings.append(group_id.split('_'))

            unique_aliases = df.columns
            # print(unique_aliases)
            # Removing None from the list of unique aliases
            unique_aliases = list(filter(None, unique_aliases))
            # Filter the aliases that are to be used for the KPI
            for alias in unique_aliases:
                for sub in substrings:
                    if all(a.strip() in alias for a in sub):
                        # print(alias)
                        filtered_aliases.append(alias)
        else:

            remove_cols = ['time_local']
            filtered_aliases = list(set(df.columns.to_list()) - set(remove_cols))

        return filtered_aliases

    @staticmethod
    def __batch_subset(batch, duration):
        """
        Gets a dataframe and a specific duration, where it takes a subset
        of dataframe that falls in the specific hours of duration.
        Parameters
        ----------
        batch: dataframe
        It's the main dataframe whose subset is to be taken based on time column.
        duration:
        A time period for which a subset of the dataframe
        will be taken.
        Returns
        -------
        batch_subset: dataframe
        A subset of the main dataframe for which timing is in between
        the specific duration of hours.
        batch_min_time: time stamp
        It's the start time of the subset dataframe
        batch_max_time: time stamp
        It's the end time of the subset dataframe.
        """
        # set min and max time variable as global
        global batch_min_time
        global batch_max_time

        # get maximum timestamp of the batch
        batch_max_time = str(arrow.get(batch['time_local'].max()).datetime).split('+')[0]
        # convert string formated timestamp to datetime object
        batch_max_time = datetime.datetime.strptime(batch_max_time, '%Y-%m-%d %H:%M:%S')

        # get minimum timestamp by considering duration hours
        batch_min_time = batch_max_time - datetime.timedelta(hours=int(duration),
                                                             minutes=int(round(duration % 1, 4) * 60))
        # get subset of data for the minimum and maximum timestamps
        batch_subset = batch[(batch.time_local >= str(batch_min_time)) & (batch.time_local <= str(batch_max_time))]

        return batch_subset

    @staticmethod
    def alias_pairs_dataframe(self, data_rd=None, aliases=None, kpi=None, resample_grain=None,
                              daily_resample=None, agg=None, non_negative=None):
        # create an empty dataframe
        df_master = pd.DataFrame()
        # get indices of aliases's elements
        res = [index for index, val in enumerate(aliases)]
        # create copy of the aliases
        alias_cols = aliases.copy()
        # append time_local into the copied alaises
        alias_cols.append('time_local')
        # get config file aliases columns having same index as res list's elements
        cols = [val for index, val in enumerate(self.__res) if index in res]
        # append time_local into the cols list
        cols.append('time_local')
        # get data for the given aliases
        df = data_rd[alias_cols].copy()
        # assign config file alias column name
        df.columns = cols
        # in case there is data for the pair
        if df.shape[0] > 0:
            # assign df to df_master
            df_master = df
        return df_master

    @staticmethod
    def alias_dataframe(self, data_rd=None, aliases=None, kpi=None, resample_grain=None,
                        daily_resample=None, agg=None, non_negative=None):
        df_master = pd.DataFrame()
        df = data_rd[['time_local', aliases]].copy()
        df.rename(columns={aliases: 'alias_a'}, inplace=True)
        if df.shape[0] > 0:
            df_master = df

        return df_master

    @staticmethod
    def __alias_pairs(self, data_rd, rule, aliases):
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

    @staticmethod
    # def message_builder(logs, data_end_time, data, client_id, logs_link, alias_value):
    #     """
    #     Gets a dataframe, that has information about the tests that are either passed of failed
    #     Parameters
    #     ----------
    #     logs_df: Dataframe
    #     This is the dataframe, which contains different tests that are performed.
    #     Returns
    #     -------
    #     message: string
    #     It contains
    #     """
    #     current_time = str(datetime.datetime.utcnow().replace(second=0, microsecond=0)) + ' UTC'
    #     message = f"*{client_id}*  {data_end_time}\n"
    #     if (len(logs.loc[logs.test == 'fail']) > 0):
    #         df_false = logs.loc[logs['test'] == 'fail']
    #         # print(df_false)
    #         rule_names = df_false.loc[df_false.criticality == 'high']['rule_name'].unique()
    #         # print(rule_names)
    #         for i in range(len(rule_names)):
    #             message = message + f"\n *{rule_names[i]}*"
    #
    #         if data.shape[0] > 0:
    #             message = message + f"\n\nDuplicate aliases"
    #             message = message + f"\n {data}"
    #
    #         message = message + f"""\n
    # <{logs_link}>
    #         """
    #     return message

    import io
    import json
    import requests
    from google.cloud import storage
    import matplotlib.pyplot as plt

    def create_and_send_image_to_slack():
        # Create a figure
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6])
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_title('Example Figure')

        # Save the figure to a bytes buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)

        # Upload the image to Google Cloud Storage
        client = storage.Client.from_service_account_json('D:\Thermosphr\outstanding-pen-377709-c37a450fe94d.json')
        bucket_name = 'faizan_bucket'
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob('example_figure.png')
        blob.upload_from_string(buf.getvalue(), content_type='image/png')

        # Get the public URL of the image
        image_url = f'https://storage.googleapis.com/{bucket_name}/{blob.name}'

        # Construct the Slack message payload
        payload = {
            "blocks": [
                {
                    "type": "image",
                    "title": {
                        "type": "plain_text",
                        "text": "Example Figure",
                        "emoji": True
                    },
                    "image_url": image_url,
                    "alt_text": "example_figure"
                }
            ]
        }

        # Send the message to the Slack channel
        SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload), headers=headers)

        if response.status_code != 200:
            raise ValueError(f'Error sending message to Slack: {response.status_code} {response.text}')

        return image_url

    def message_builder(data_end_time, data, client_id, logs_link, rule_name, aliases):
        # Generate the message string
        message = f"*{client_id}*  {data_end_time}\n"
        message += f"\n *{rule_name}* \n   {aliases}"
        message += f"\n<{logs_link}>"

        # Create and send the image to Slack
        image_url = create_and_send_image_to_slack()

        # Add the image URL to the message string
        message += f"\n\nHere's an example figure: {image_url}"

        return message

    # def message_builder( data_end_time, data, client_id, logs_link,rule_name, aliases):
    #     """
    #     Gets a dataframe, that has information about the tests that are either passed of failed
    #     Parameters
    #     ----------
    #     logs_df: Dataframe
    #     This is the dataframe, which contains different tests that are performed.
    #     Returns
    #     -------
    #     message: string
    #     It contains
    #     """
    #
    #     message = f"*{client_id}*  {data_end_time}\n"
    #     message = message + f"\n *{rule_name}* \n   {aliases}"
    #     message = message + f"""\n
    # <{logs_link}>
    #         """
    #     return message


    def slack_alert(message):
        """
        Send a message to a Slack channel using a webhook URL.

        Parameters:
        webhook_url (str): The URL of the Slack webhook.
        message (str): The message to send to the Slack channel.

        Returns:
        None
        """
        slack_data = {'text': message}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(SLACK_WEBHOOK, data=json.dumps(slack_data), headers=headers)

        if response.status_code != 200:
            raise ValueError(f'Error sending message to Slack: {response.status_code} {response.text}')

    def return_log(self):
        return self.__df_logs