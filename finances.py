import extract_time
import pandas as pd

def outgoings(user_data:pd.DataFrame):

    ''' '''
    df = user_data.copy()
    df_outgoings = df[df.type=='DEBIT']
    outgoings = round(0-df_outgoings['amount'].sum(),2)

    return outgoings

def income(user_data:pd.DataFrame):

    ''' '''
    df = user_data.copy()
    df_income = df[df.type=='CREDIT']
    income = round(df_income['amount'].sum(),2)

    return income


def essential_outgoings(user_data:pd.DataFrame):

    ''' '''
    df = user_data.copy()
    df_essentials=df[(df.need_want=='Essential')|((df.transaction_class=='Loans&Credit')&(df.type=='DEBIT'))]
    essentials = round(0-df_essentials['amount'].sum(),2)

    return essentials

def monthly_essentials(user_data:pd.DataFrame):

    ''' '''

    df = user_data.copy()
    #create monthly time bins
    df_dates = extract_time.create_time_bins(df,'M')
    outgoings = []

    for i in df_dates.index:
        start = pd.Timestamp(df_dates.iloc[i]['per_start'])
        end =  pd.Timestamp(df_dates.iloc[i]['per_end'])
        # create df containing all dates within the time bin parameters
        df_month = df[(df.timestamp.dt.date>=start)&(df.timestamp.dt.date<end)]
        # calculate total essential outgoings for the period
        ess_out = round(0-(df_month[(df_month.need_want=='Essential')|((df_month.transaction_class=='Loans&Credit')&(df_month.type=='DEBIT'))]['amount'].sum()),2)
        outgoings.append(ess_out)
    #print(f'average monthly essential spend: £{np.mean(outgoings)}')
    monthly_essentials=np.mean(outgoings)

    return monthly_essentials

    # Average balance for the month
    # Credit turnover for the month (amount coming in per month)
    # Balance at the end of the month
    # minimum balance attained during the month
    # maximum balance attained during the month
    # current overdraft excess (amount by which overdraft has been exceeded)
    # frequency of overdraft use
    # overdraft balance at end of each month