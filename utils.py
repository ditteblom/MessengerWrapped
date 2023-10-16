import pandas as pd
import json
import re
from functools import partial
import datetime
import unicodedata
import glob

# functions for dataframe
def no_reactions(string):
    try:
        out = len(string)
    except:
        out = 0
    return out

def type_reactions(string):
    lst = []
    try:
        for item in string:
            lst.append(unicodedata.name(item['reaction']))
        tmp = [*{*lst}]
        out = ''
        for item in tmp:
            out += str(item).lower() + ','
    except:
        out = float('nan')
    return out

def create_df(path_from_user):
    '''
    Input: path(s) for files containing facebook messages.
    Output: dataframe with content and list with participants.
    '''
    paths = glob.glob(path_from_user + '/message*.json')
    df = pd.DataFrame()

    for path in paths:
        fix_mojibake_escapes = partial(
            re.compile(rb'\\u00([\da-f]{2})').sub,
            lambda m: bytes.fromhex(m[1].decode()),
        )

        with open(path, 'rb') as binary_data:
            repaired = fix_mojibake_escapes(binary_data.read())
        data = json.loads(repaired)

        tmp = pd.DataFrame(data['messages'])
        df = pd.concat([df,tmp])

    df.reset_index(inplace = True, drop=True)
    df['timestamp_ms'] = df['timestamp_ms'].apply(lambda x : datetime.datetime.fromtimestamp(x/1000.0))
    df.rename(columns={"timestamp_ms": "timestamp"}, inplace = True)
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    df['time'] = pd.to_datetime(df['timestamp']).dt.time
    df['year'] = pd.to_datetime(df['timestamp']).dt.year
    df['month'] = pd.to_datetime(df['timestamp']).dt.month
    df['weekday'] = pd.to_datetime(df['date']).dt.day_name()
    df['no_reactions'] = df.reactions.apply(lambda x: no_reactions(x))
    df['type_reactions'] = df.reactions.apply(lambda x: type_reactions(x))

    participants = []
    for item in data['participants']:
        participants.append(item['name'])

    df.sort_values(by='timestamp', inplace=True)
    df.reset_index(inplace = True, drop=True)

    return df, participants