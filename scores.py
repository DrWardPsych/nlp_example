import pandas as pd
import numpy as np
from datetime import date
import extract_time
import importlib
import f_wellbeing
importlib.reload(f_wellbeing)

def score_profile(user_data:pd.DataFrame):

    data = user_data.copy()

    feature_list=['income','outgoings','budgeting score','affordability','preparedness','bnpl count']
    scores_list=[]
    scores_dict={}
    scores_dict['timestamp']=date.today().strftime("%d-%b-%Y")

    for feature in feature_list:
        scores_dict[feature]=weekly_score(data,feature)
        scores_list.append(weekly_score(data,feature))

    wellbeing_scores=[]

    if 100-scores_dict['affordability']>=75:
        wellbeing_scores.append(0)
    elif (100-scores_dict['affordability']<75)&(100-scores_dict['affordability']>=1):
        wellbeing_scores.append(1)
    elif 100-scores_dict['affordability']==0:
        wellbeing_scores.append(2)

    if scores_dict['preparedness']<=25:
        wellbeing_scores.append(0)
    elif (scores_dict['preparedness']>25)&(scores_dict['preparedness'])<=99:
        wellbeing_scores.append(1)
    else:
        wellbeing_scores.append(2)

    if scores_dict['bnpl count']==0:
        wellbeing_scores.append(0)
    else:
        wellbeing_scores.append(1)

    observed_wellbeing = sum(wellbeing_scores)*(100/5)

    scores_dict['observed wellbeing'] = observed_wellbeing

    return scores_dict

def weekly_score(df:pd.DataFrame,measure:str):
    
    ''' '''

    measure_score=[]   
    df_dates = extract_time.create_time_bins(df)
    #print(df_dates.index)
    for i in df_dates.index:

        if measure == 'outgoings':
            start = pd.Timestamp(df_dates.iloc[i]['per_start'])
            end =  pd.Timestamp(df_dates.iloc[i]['per_end'])
            df_week = df[(df.timestamp.dt.date>=start)&(df.timestamp.dt.date<end)]
            score = outgoings(df_week)
            measure_score.append(score)

        elif measure == 'essential outgoings':
            start = pd.Timestamp(df_dates.iloc[i]['per_start'])
            end =  pd.Timestamp(df_dates.iloc[i]['per_end'])
            df_week = df[(df.timestamp.dt.date>=start)&(df.timestamp.dt.date<end)]
            score = essential_outgoings(df_week)
            measure_score.append(score)

        elif measure == 'budgeting score':                                                      ## <-- can this go into a dict??
            start = pd.Timestamp(df_dates.iloc[i]['per_start'])
            end =  pd.Timestamp(df_dates.iloc[i]['per_end'])
            df_week = df[(df.timestamp.dt.date>=start)&(df.timestamp.dt.date<end)]
            score = budgeting_score(df_week)
            measure_score.append(score)

        elif measure == 'income':
            start = pd.Timestamp(df_dates.iloc[i]['per_start'])
            end =  pd.Timestamp(df_dates.iloc[i]['per_end'])
            df_week = df[(df.timestamp.dt.date>=start)&(df.timestamp.dt.date<end)]
            score = income(df_week)
            measure_score.append(score)

        elif measure == 'affordability':
            start = pd.Timestamp(df_dates.iloc[i]['per_start'])
            end =  pd.Timestamp(df_dates.iloc[i]['per_end'])
            df_week = df[(df.timestamp.dt.date>=start)&(df.timestamp.dt.date<end)]
            score = f_wellbeing.affordability(df_week)
            measure_score.append(score)

        elif measure == 'preparedness':
            start = pd.Timestamp(df_dates.iloc[i]['per_start'])
            end =  pd.Timestamp(df_dates.iloc[i]['per_end'])
            df_week = df[(df.timestamp.dt.date>=start)&(df.timestamp.dt.date<end)]
            score = f_wellbeing.preparedness(df_week,monthly_essentials(df))
            measure_score.append(score)

        elif measure == 'bnpl count':
            start = pd.Timestamp(df_dates.iloc[i]['per_start'])
            end =  pd.Timestamp(df_dates.iloc[i]['per_end'])
            df_week = df[(df.timestamp.dt.date>=start)&(df.timestamp.dt.date<end)]
            score = f_wellbeing.BNPL(df_week)
            if score > 0:
                measure_score.append(score)
            else:
                measure_score.append(0)


    
    df_dates['score']=measure_score
    df_dates[f'rolling {measure}']=round(df_dates['score'].rolling(4).mean().fillna(df_dates.score.mean()),2)
    df_dates = df_dates.rename(columns={'score':f'{measure}'})   
    current_score = round(sum(measure_score[-4:])/4)

    #print(f'Average {measure} for past 4 weeks: {current_score}')

    #print(f'Your budgeting score on {date.today().isoformat()} is {round(sum(b_score[-4:])/4)}. The maximum attainable score is 100')
    
    return current_score


def budgeting_score(user_data):

    ''' '''
   
    df_week = pd.DataFrame(user_data[user_data.type=='DEBIT'].groupby('need_want')['amount'].sum()).reset_index().rename(columns={'need_want':'classification'})
    df = df_week.copy()
    df.amount=0-df.amount
    df=df[df.classification!='Unknown'].reset_index(drop=True)

    expected_rows = ['Wants','Essentials','Future You']
    ideals = {'Essential':50,'Want':30,'Future You':20}


    for i in expected_rows:
        if i not in list(df.classification):
            df.loc[len(df)]=[str(i),0]
    
    df['Ideal_prop']=df.classification.map(ideals)

    try:
        df['prop_spend']=100*(df.amount/sum(df.amount))
    except ZeroDivisionError:
        df['prop_spend']=0

    df['ideal_diff']=0
    df.loc[(df.classification=='Wants')|(df.classification=='Essentials'),'ideal_diff']=df.Ideal_prop-df.prop_spend
    df.loc[df.classification=='Future You','ideal_diff']=df.Ideal_prop-df.prop_spend
    df.ideal_diff = df.ideal_diff.fillna(0)
    
    for i,j in enumerate(df.ideal_diff):

        if j<0:
            df.ideal_diff.iloc[i]=0-df.ideal_diff.iloc[i]
            
            
    budgeting_score = round(100-sum(df.ideal_diff))
    #ideal_save=round(sum(df.amount)*0.2)
    #ideal_essentials=round(sum(df.amount)*0.5)
    #ideal_wants=round(sum(df.amount)*0.3)


    #print(f'Your budgeting score on {date.today().isoformat()} is {budgeting_score}. The maximum attainable score is 100')
    #print(f'The perfect budgeting score for this period would be achieved by spending £{ideal_essentials} on essentials and investing £{ideal_save} in your future self, which would leave £{ideal_wants} for fun!')

    return budgeting_score


def outgoings(df):

    ''' '''
    
    df_outgoings = df[df.type=='DEBIT']
    outgoings = round(0-df_outgoings['amount'].sum(),2)

    return outgoings

def income(df):

    ''' '''
    
    df_income = df[df.type=='CREDIT']
    income = round(df_income['amount'].sum(),2)

    return income


def essential_outgoings(df):

    ''' '''

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