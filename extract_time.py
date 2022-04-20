import pandas as pd
from datetime import timedelta


def create_time_bins(user_data:pd.DataFrame,timescale:str='W'):

    ''' 
    
    Function creates weekly or monthly timebins to aggregate scores and transaction data.
    
        Args:
            user_data: pd.DataFrame containing processed transaction data including risk flags, BNPL, classifications.
            timescale: size of timebins (week 'W', month 'M')
            
        Returns:
            scores_time: pd.DataFrame containing start and end dates for each time bin 
            
    '''

    if timescale == 'W':
        days = 6

    elif timescale == 'M':
        days = 28
        
    df = user_data.copy()

    scores_time = pd.DataFrame(columns=['per_start','per_end','score'])
    starts=[]

    start = pd.to_datetime(get_key_dates(df)['oldest transaction'][0])
    end = pd.to_datetime(get_key_dates(df)['recent transaction'][0])
    week_starts = list(pd.date_range(start,end,freq=timescale))
    for start in week_starts:
        starts.append(start)

    scores_time['per_start']=starts
    scores_time['per_end']=pd.to_datetime(scores_time.per_start+timedelta(days=days))


    return scores_time

def get_key_dates(user_data):

    ''' 
    
    Function creates dictionary of key dates to support create_time_bins function 
    
        Args:
            user_data: pd.DataFrame containing processed transaction data including risk flags, BNPL, classifications.
            
        Returns:
            dates (dict): dictionary containing key dates (oldest transaction, most recent transaction, start of last month, start of last week, last full day) 
            
    '''

    df = user_data.copy()

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


