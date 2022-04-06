import pandas as pd
import pickle
from datetime import date
import extract_time


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
    ideal_save=round(sum(df.amount)*0.2)
    ideal_essentials=round(sum(df.amount)*0.5)
    ideal_wants=round(sum(df.amount)*0.3)


    #print(f'Your budgeting score on {date.today().isoformat()} is {budgeting_score}. The maximum attainable score is 100')
    #print(f'The perfect budgeting score for this period would be achieved by spending £{ideal_essentials} on essentials and investing £{ideal_save} in your future self, which would leave £{ideal_wants} for fun!')

    return budgeting_score

def weekly_score(df):

    b_score=[]   
    df_dates = extract_time.create_time_bins(df)
    for i in df_dates.index:
        start = pd.Timestamp(df_dates.iloc[i]['per_start'])
        end =  pd.Timestamp(df_dates.iloc[i]['per_end'])
        df_week = df[(df.timestamp.dt.date>=start)&(df.timestamp.dt.date<end)]
        score = budgeting_score(df_week)
        b_score.append(score)
    #print(b_score)
    df_dates['score']=b_score
    df_dates['rolling_average']=df_dates['score'].rolling(4).mean().fillna(df_dates.score.mean())   
    current_score = round(sum(b_score[-4:])/4)

    print(f'Budgeting score: {current_score}')

    print(f'Your budgeting score on {date.today().isoformat()} is {round(sum(b_score[-4:])/4)}. The maximum attainable score is 100')
    
    return df_dates