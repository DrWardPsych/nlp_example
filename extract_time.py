import pandas as pd
from datetime import timedelta


def create_time_bins(user_data:pd.DataFrame,timescale:str='W'):

    df = user_data.copy()

    scores_time = pd.DataFrame(columns=['per_start','per_end','score'])
    starts=[]

    start = pd.to_datetime(get_key_dates(df)['oldest transaction'][0])
    end = pd.to_datetime(get_key_dates(df)['recent transaction'][0])
    week_starts = list(pd.date_range(start,end,freq=timescale))
    for start in week_starts:
        starts.append(start)

    scores_time['per_start']=starts
    scores_time['per_end']=pd.to_datetime(scores_time.per_start+timedelta(days=6))

    #start = pd.to_datetime(scores_time.iloc[0]['per_start'])
    #end =  pd.to_datetime(scores_time.iloc[0]['per_end'])

    return scores_time

def get_key_dates(user_data):

    ''' '''

    df = user_data   

    oldest_transaction = df.timestamp.dt.date.min(),
    recent_transaction = df.timestamp.dt.date.max(),
    last_month_start = df.timestamp.dt.date.max()-timedelta(days=28),
    last_week_start = df.timestamp.dt.date.max()-timedelta(days=7),
    last_day_start = df.timestamp.dt.date.max()-timedelta(days=1)

    dates={'oldest transaction':oldest_transaction,
            'recent transaction':recent_transaction,
            'last month': last_month_start,
            'last week':last_week_start,
            'last full day':last_day_start}

    return dates


