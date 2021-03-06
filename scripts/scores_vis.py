import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np
import pandas as pd
import seaborn as sns
import extract_time


def budget_pie(user_data):

    ''' '''
        
    df = pd.DataFrame(user_data[user_data.type=='DEBIT'].groupby('need_want')['amount'].sum()).reset_index().rename(columns={'need_want':'classification'})
    df.amount=0-df.amount
    df=df[df.classification!='Unknown'].reset_index()

    #colours = ['GreenYellow','Yellow','HotPink']
    labels = ['Essential','Future You','Want']

    cdict={'Essential':'Aquamarine',
           'Future You':'Yellow',
           'Want':'HotPink'}

    fracs = [50, 20, 30]

    plt.rcParams['patch.edgecolor'] = 'black'
    fig = plt.figure()
     
    ax1 = fig.add_axes([0,0,1,1])
    ax1.axis('equal')
    ax1.pie(df.amount, labels = df.classification,colors=[cdict[key]for key in df.classification], autopct='%1.1f%%',radius = 1.2)

    ax2 = fig.add_axes([1,0,1,1])
    ax2.axis('equal')
    ax2.pie(fracs, labels=labels, colors=[cdict[key]for key in labels], autopct='%1.1f%%', explode =[0,0,0.05],shadow=True,radius = 1.2)

    ax1.set_title('Your outgoings',y=0.6)
    ax2.set_title('Your Ideal outgoings',y=0.6)

    plt.show()

def spend_bar(user_data):

    ''' '''

    df = pd.DataFrame(user_data[user_data.type=='DEBIT'].groupby('transaction_class')['amount'].sum()).reset_index()
    df.amount=0-df.amount
    
    df=df[df.transaction_class!='unknown'].reset_index().sort_values(by='amount',ascending=False).copy()
    
    fig = plt.figure(figsize=[8,8])
    ax = fig.add_axes([0,0,1,1])
    ax.bar(df.transaction_class,100*(df.amount/sum(df.amount)))
    plt.xticks(rotation=90)
    
    plt.show()

def weekly_b_score(df:pd.DataFrame,measure:str):    

    ''' '''
    # set figure size
    plt.figure( figsize = ( 12, 8))

    df = df.copy()
    
    # plot a simple time series plot
    sns.lineplot( x = 'per_end',
                y = measure,
                data = df,
                color='hotpink',
                label = f'Weekly {measure}')
    
    # # plot using rolling average
    
    sns.lineplot( x = 'per_end',
                y = f'rolling {measure}',
                data = df,
                color='aquamarine',
                label = 'Rollingavg')
    
    plt.xlabel('Weeks before using GW app')
    
    # setting customized ticklabels for x axis
    pos = [ '2021-12-18', '2021-12-25', '2022-01-01','2022-01-08','2022-01-15','2022-01-22',
    '2022-01-29','2022-02-05','2022-02-12','2022-02-19','2022-02-26','2022-03-05','2022-03-12']

    
    lab = pd.Series(pos).index[::-1]
    
    plt.xticks( pos, lab)
    plt.ylabel(f'{measure}')


def weekly_score_smooth(df:pd.DataFrame,measure:str):    

    ''' '''
    # set figure size
    plt.figure( figsize = ( 12, 8))

    df = df.copy()
    x1 = df.per_end.index
    y1 = df[measure]

    xnew = np.linspace(x1.min(), x1.max(), 200)

    spl = make_interp_spline(x1, y1, k=5)
    y_smooth = spl(xnew)

    plt.plot(xnew,y_smooth)

    df = df.copy()
    x2 = df.per_end.index
    y2 = df[f'rolling {measure}']

    xnew2 = np.linspace(x2.min(), x2.max(), 200)

    spl2 = make_interp_spline(x2, y2, k=5)
    y_smooth2 = spl2(xnew)

    plt.plot(xnew2,y_smooth2)


    # # plot a simple time series plot
    # sns.lineplot( x = xnew,
    #             y = y_smooth,
    #             data = df,
    #             color='hotpink',
    #             label = f'Weekly {measure}')
    
    # # # plot using rolling average
    
    # sns.lineplot( x = 'per_end',
    #             y = f'rolling {measure}',
    #             data = df,
    #             color='aquamarine',
    #             label = 'Rollingavg')
    
    # plt.xlabel('Weeks before using GW app')
    
    # # setting customized ticklabels for x axis
    # pos = [ '2021-12-18', '2021-12-25', '2022-01-01','2022-01-08','2022-01-15','2022-01-22',
    # '2022-01-29','2022-02-05','2022-02-12','2022-02-19','2022-02-26','2022-03-05','2022-03-12']

    
    # lab = pd.Series(pos).index[::-1]
    
    # plt.xticks( pos, lab)
    # plt.ylabel(f'{measure}')