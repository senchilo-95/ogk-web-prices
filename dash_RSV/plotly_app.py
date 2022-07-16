import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from django_plotly_dash import DjangoDash
import sqlalchemy as sa
from .datasets import df_st
engine = sa.create_engine('sqlite:///db.sqlite3')
connection=engine.connect()



app = DjangoDash('SimpleExample')   # replaces dash.Dash
# df_st=df_h.copy()
dict_dates = {1:'янв',2:'фев',3:'мар',4:'апр',5:'мая',6:'июн',7:'июл',8:'авг',9:'сен',10:'окт',11:'ноя',12:'дек'}
range_of_dates=pd.date_range(start=df_st.index[0].date(),end=df_st.index[-1].date(),freq='1D')
dates_list = ['{} {}'.format(idx.day,dict_dates[idx.month]) for idx in range_of_dates]
df_st_m = df_st.resample('1D').mean()
dropdown = dcc.Dropdown(
    id = 'station-dropdown',
    searchable=False,
    value='Киришская ГРЭС',
    options=[
{'label' : 'Все станции', 'value' : df_st.columns},
{'label' : 'Киришская ГРЭС', 'value' : 'Киришская ГРЭС'},
{'label' : 'Псковская ГРЭС', 'value' : 'Псковская ГРЭС'},
{'label' : 'Череповецкая ГРЭС', 'value' : 'Череповецкая ГРЭС'},
{'label' : 'Рязанская ГРЭС', 'value' : 'Рязанская ГРЭС'},
{'label' : 'Новочеркасская ГРЭС', 'value' : 'Новочеркасская ГРЭС'},
{'label' : 'Ставропольская ГРЭС', 'value' : 'Ставропольская ГРЭС'},
{'label' : 'Троицкая ГРЭС', 'value' : 'Троицкая ГРЭС'},
{'label' : 'Сургутская ГРЭС-1', 'value' : 'Сургутская ГРЭС-1'},
{'label' : 'Адлерская ТЭС', 'value' : 'Адлерская ТЭС'},
{'label' : 'Грозненская ТЭС', 'value' : 'Грозненская ТЭС'},
{'label' : 'Серовская ГРЭС', 'value' : 'Серовская ГРЭС'}
    ],style={'width':'400px', 'align-items': 'center', 'justify-content': 'center'}
)

slider=dcc.Slider(len(df_st_m)-14, len(df_st_m)-1,1, value=len(df_st_m)-1,
    marks={idx:'{} {}'.format(df_st_m.index[idx].day,dict_dates[df_st_m.index[idx].month]) for idx in range(len(df_st_m)-14,len(df_st_m))},
    included=False,
    id='date_slider'
)
slider = html.Div([slider], style={'height': '50px'})
day_prices = dbc.Card([dcc.Graph(id='my-graph1')],style={"width": "98%",'margin':'5px'})
hour_prices = dbc.Card([dcc.Graph(id='my-graph2'),dbc.CardBody(slider)],style={"width": "98%",'margin':'5px'})

cards = dbc.Col([
        dbc.Row(day_prices),
        dbc.Row(hour_prices)
                ])
app.layout = html.Div([dropdown,cards],style={'background-color': '#D0DBEA'})

# # график для прогноза цен
@app.callback([Output('my-graph1', 'figure'),Output('my-graph2', 'figure')],
              [Input('station-dropdown', 'value'),Input('date_slider', 'value')])
def update_graph(tab,date):
    figure = px.line(
                 df_st[tab].resample('1D').mean(),
                title="Среднесуточные цены РСВ",
                labels={
               "date_new": "Дата. Выберите период.",
                 "value": "Цена РСВ, руб/МВт*ч",
                    'variable':'Станция'
                    },
                template="plotly_white")
    figure.update_xaxes(
        dtick="D",
        tickformat="%d%b",
        rangeslider_visible=True,
        showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3'
        )
    figure.update_yaxes(showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3')
    date_for_slider = df_st_m.index[date]
    y=date_for_slider.year
    m=date_for_slider.month
    d=date_for_slider.day
    df_st_h = df_st[(df_st.index.year==y)&(df_st.index.month==m)&(df_st.index.day==d)]
    figure_2 = px.line(
                df_st_h[tab],
                title="Почасовые цены РСВ",
                labels={
               "date_new": "Дата",
                 "value": "Цена РСВ, руб/МВт*ч",
                    'variable':'Станция'
                    },template="plotly_white")
    figure_2.update_xaxes(
        ticktext=[i for i in range(24)],
        showgrid=True,showline=True, linewidth=0.5, linecolor='black', gridcolor='#DDE6F3')
    figure_2.update_yaxes(showgrid=True,showline=True, linewidth=0.5, linecolor='black', gridcolor='#DDE6F3')

    figure.update_layout(height=400,showlegend=False)
    figure_2.update_layout(height=400,showlegend=False)
    return figure,figure_2
#

