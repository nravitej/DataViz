import numpy as np
import pandas as pd
from dash import dash, html, dcc
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import collections

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

NFPriceList=pd.read_csv('C:/Users/RAVITEJA/Downloads/netflix_price_in_different_countries.csv')
#print (NFPriceList)
McDonaldsPriceList=pd.read_csv("C:/Users/RAVITEJA/Downloads/McDPriceListCountryWise.csv")

McDonaldsPriceList["BigMac"]=McDonaldsPriceList["BigMac"].apply(lambda x:x[1:])
McDonaldsPriceList["BigMac"]=McDonaldsPriceList["BigMac"].astype(float)
McDonaldsPriceList["Fries"]=McDonaldsPriceList["Fries"].apply(lambda x:x[1:])
McDonaldsPriceList["Fries"]=McDonaldsPriceList["Fries"].astype(float)
McDonaldsPriceList["Coke"]=McDonaldsPriceList["Coke"].apply(lambda x:x[1:])
McDonaldsPriceList["Coke"]=McDonaldsPriceList["Coke"].astype(float)
McDonaldsPriceList["Meal"]=McDonaldsPriceList["Meal"].apply(lambda x:x[1:])
McDonaldsPriceList["Meal"]=McDonaldsPriceList["Meal"].astype(float)

NFPriceList["Total Library Size"]=NFPriceList["Total Library Size"].astype(float)
NFPriceList.iloc[::,::]=NFPriceList.iloc[::,::].astype(object)
McDonaldsPriceList.iloc[::,::]=McDonaldsPriceList.iloc[::,::].astype(object)
#print(NFPriceList.dtypes)
#print(McDonaldsPriceList.dtypes)
#STATS=NFPriceList.iloc[::,[0,6]].join(McDonaldsPriceList,on='Country',lsuffix='_NF',rsuffix='_MD',how='inner')
#print(STATS.iloc[::,[1,7,9]])
NFP={}
MDP={}
NFP["Country"]=NFPriceList["Country"].values
NFP["PremiumSubscription"]=(NFPriceList["Cost Per Month - Premium ($)"].values).astype(int)
MDP["Country"]=McDonaldsPriceList["Country"].values
MDP["BigMac"]=McDonaldsPriceList["BigMac"].values

#print(NFP["Country"].size)
#print(NFP["Country"][64])
k=np.zeros(NFP["Country"].size)


for i in range((NFP["Country"].size)):
    for j in range((MDP["Country"].size)):
        if(NFP["Country"][i]==MDP["Country"][j]):
            k[i]=(MDP["BigMac"][j])





NFP["BigMac"]=np.array(k.copy())
#print(NFP["BigMac"].size)

Proportion=np.zeros(NFP["Country"].size)
for i in range((NFP["Country"].size)):
    if (NFP["BigMac"][i]!=0.0 or NFP["BigMac"][i]!=0):
        Proportion[i]=(NFP["PremiumSubscription"][i])/(NFP["BigMac"][i])


NPBM=collections.Counter(NFP["PremiumSubscription"]-(NFP["BigMac"]).astype(int))
print(NPBM)
fig4=px.pie(NFP, values=NPBM.values(),names=NPBM.keys(),  title='Price diff BigMac and Netflix Subscription')

#print(MDP)
fig2=px.histogram(NFPriceList,y="Cost Per Month - Premium ($)",x="Country",color=NFPriceList["Cost Per Month - Premium ($)"])
fig3= go.Figure()
fig3.add_trace(go.Bar(x=NFPriceList["Country"],y=NFPriceList["Cost Per Month - Premium ($)"],name='NetFlixPremium',marker_color='indianred'))
fig3.add_trace(go.Bar(x=NFPriceList["Country"],y=NFPriceList["Cost Per Month - Basic ($)"],name='NetFlixBasic',marker_color='Blue'))
fig3.add_trace(go.Bar(x=NFPriceList["Country"],y=NFPriceList["Cost Per Month - Standard ($)"],name='NetFlixStandard',marker_color='Green'))

MeanPremium=(NFPriceList["Cost Per Month - Premium ($)"].mode()).astype(int)
MeanNoMovies=NFPriceList["No. of Movies"].mode()
print(MeanPremium)
print(MeanNoMovies)


#fig3=px.histogram(y=NFPriceList["Cost Per Month - Premium ($)"],x=NFPriceList["Country"])
#fig4=px.pie(MDP, values='BigMac', names='Country', title='MCD Big Mac Price',hole=0.5)


Frequency=collections.Counter(NFP["PremiumSubscription"])
print(Frequency)
fig1 = px.pie(NFP, values=Frequency.values(),names=Frequency.keys(),  title='NetflixPriceList')
#NFPriceList[NFPriceList["Total Library Size"].sort_values]
fig6=px.line(NFPriceList.sort_values(by='Total Library Size'),x='Total Library Size',y='Cost Per Month - Premium ($)',title='Library Size vs Premium Price')
fig7=px.scatter(NFPriceList.sort_values(by='Total Library Size'),x='Total Library Size',y='Cost Per Month - Premium ($)',title='Library Size vs Premium Price')

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H2(children='Netflix Premium vs BigMac'),
        html.Div(children='''
            Bar Chart (Total Score)
        '''),
        dcc.Graph(id='example-graph',
        figure={
            'data': [
                {'x': NFP["Country"], 'y': NFP["PremiumSubscription"], 'type': 'bar', 'name': 'PremiumSubscription'},
                {'x': NFP["Country"], 'y': NFP["BigMac"], 'type': 'bar', 'name': 'BigMac'}
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
        ),
    ]),
html.Div([
        html.H2(children='Netflix Premium Price Distribution'),
        html.Div(children='''
             Bar Chart (Price)
         '''),
        dcc.Graph(
            id='graph2',
            figure=fig2
        ),
    ]),
html.Div([
        html.H2(children='All Suscription Analysis Netflix'),
        html.Div(children='''
             Bar Chart (Netflix Suscription Price)
         '''),
        dcc.Graph(
            id='graph3',
            figure=fig3
        ),
    ]),
html.Div([
        html.H2(children='Premium Subscription Frequency Coverage'),
        html.Div(children='''
             
         '''),
        dcc.Graph(
            id='graph4',
            figure=fig1
        ),
    ]),
html.Div([
        html.H2(children='How Economical the Subscription price'),
        html.Div(children='''
             
         '''),
        dcc.Graph(
            id='graph5',
            figure=fig4
        ),
    ]),
html.Div([
        html.H2(children='Premium Subscription vs No of Libraries'),
        html.Div(children='''
             
         '''),
        dcc.Graph(
            id='graph6',
            figure=fig6
        ),
        dcc.Graph(
            id='graph7',
            figure=fig7
        ),

    ]),



])

if __name__ == '__main__':
    app.run_server(debug=True)