import pandas as pd
import scores



def observed_wellbeing():
    pass

def affordability(user_data:pd.DataFrame):

    ''' '''

    df_week = user_data.drop_duplicates(subset='timestamp',keep='last').copy()

    daily_affordability=[]
    
    for bal in df_week['runningBalance.amount']:
        ## if current balance before essential outgoings is less than rolling average essential outgoings, 1 is added to affordability score
        if bal+scores.essential_outgoings(user_data) < scores.essential_outgoings(user_data):
            daily_affordability.append(1)
        else:
            daily_affordability.append(0)

        affordability = round(100-(sum(daily_affordability)/len(df_week)*100),2) ## <- the close the affordability score is to 100, the better

    return affordability


def preparedness(user_data:pd.DataFrame,essential_spend:float):

    ''' '''

    df = user_data.copy()
    #df_prep = user_data.drop_duplicates(subset='timestamp',keep='last')
    monthly_essentials=essential_spend
    prepared = []
    for balance in df['runningBalance.amount']:
        # if the daily balance is greater than or equal to monthly essential outgoings add 1 point
        
        if balance >= monthly_essentials:
            prepared.append(1)
        else:
            prepared.append(0)

    df['preparedness_points'] = prepared
    df_prep = df.drop_duplicates(subset='timestamp',keep='last')
    #print(f'% of days since {str(df_deduped.timestamp.min()).split()[0]} where balance would cover monthly outgoings: {round(100*(sum(df_deduped.preparedness_points))/len(df_deduped),2)}%')
    prepared_days = round(100*(sum(df_prep.preparedness_points))/len(df_prep),2)
    
    return prepared_days

# def age_norm_savings():
#
#     ''' '''
#
#     pass

def overdraft():

    ''' '''

    pass

def charges():

    ''' '''

    pass


def BNPL():

    ''' '''

    pass