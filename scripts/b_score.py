import pandas as pd



def budgeting_score(user_data):

    ''' Essentials, wants and future investments are calculated as a proportion of weekly spend, expressed as a ratio (e.g. 40:30:30). A weekly budgeting score is derived as the deviation of this ratio away from the ideal spend ratio of 50:30:20 for Essentials, Wants, and Future, respectively. 
        In order to capture a long-term view of users’ budgeting skill, the overall budgeting score is calculated as the average of the prior 12 weeks’ budgeting scores, recalculated each time the user refreshes their transaction data.  
    '''
   
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