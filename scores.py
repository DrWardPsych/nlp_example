import pandas as pd
import numpy as np
from datetime import date
import extract_time
import importlib
import f_wellbeing
import finances
import b_score
importlib.reload(f_wellbeing)
importlib.reload(extract_time)

def score_profile(user_data:pd.DataFrame):

    ''' Function creates user score profile and exports as a dictionary. Still under development '''

    data = user_data.copy()

    feature_list=['income','outgoings','budgeting score','affordability','preparedness','bnpl count']
    scores_list=[]
    scores_dict={}
    scores_dict['timestamp']=date.today().strftime("%d-%b-%Y")

    for feature in feature_list:
        scores_dict[feature]=weekly_score(data,feature)
        scores_list.append(weekly_score(data,feature))

    wellbeing_scores=[]

    # affordability metric
    if 100-scores_dict['affordability']>=75:
        wellbeing_scores.append(0)
    elif (100-scores_dict['affordability']<75)&(100-scores_dict['affordability']>=1):
        wellbeing_scores.append(1)
    elif 100-scores_dict['affordability']==0:
        wellbeing_scores.append(2)

    # preparedness metric
    if scores_dict['preparedness']<=25:
        wellbeing_scores.append(0)
    elif (scores_dict['preparedness']>25)&(scores_dict['preparedness'])<=99:
        wellbeing_scores.append(1)
    else:
        wellbeing_scores.append(2)

    # BNPL metric
    if scores_dict['bnpl count']==0:
        wellbeing_scores.append(0)
    else:
        wellbeing_scores.append(1)

    # Compute overall observed financial wellbeing score
    observed_wellbeing = sum(wellbeing_scores)*(100/5)
    scores_dict['observed wellbeing'] = observed_wellbeing

    return scores_dict

def weekly_score(df:pd.DataFrame,measure:str):
    
    ''' '''

    measure_score=[]   
    df_dates = extract_time.create_time_bins(df)
   
    for i in df_dates.index:

        start = pd.Timestamp(df_dates.iloc[i]['per_start'])
        end =  pd.Timestamp(df_dates.iloc[i]['per_end'])
        df_week = df.loc[(df.timestamp.dt.date>=start)&(df.timestamp.dt.date<end)].copy()

        method_dict={'outgoings':finances.outgoings(df_week),
                 'essential outgoings':finances.essential_outgoings(df_week),
                 'budgeting score':b_score.budgeting_score(df_week),
                 'income':finances.income(df_week),
                 'affordability':f_wellbeing.affordability(df_week),
                 'preparedness':f_wellbeing.preparedness(df_week,finances.monthly_essentials(df)),
                 'bnpl count':f_wellbeing.BNPL(df_week)}

        if measure in method_dict:
            score = method_dict.get(measure)
            if score > 0:
                measure_score.append(score)
            else:
                measure_score.append(0)

    
    df_dates['score']=measure_score
    df_dates[f'rolling {measure}']=round(df_dates['score'].rolling(4).mean().fillna(df_dates.score.mean()),2)
    df_dates = df_dates.rename(columns={'score':f'{measure}'})   
    current_score = round(sum(measure_score[-4:])/4)

    return df_dates,current_score


