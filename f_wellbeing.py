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


def preparedness():

    ''' '''
    pass

def age_norm_savings():
    pass

def default_charges():
    pass

def BNPL():
    pass