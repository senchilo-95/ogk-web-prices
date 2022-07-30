from dash import dash_table
import plotly.figure_factory as ff
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import sqlalchemy as sa
from .datasets import df_st
import locale
from .navbar import Navbar
nav = Navbar()

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


dict_dates = {1:'янв',2:'фев',3:'мар',4:'апр',5:'мая',6:'июн',7:'июл',8:'авг',9:'сен',10:'окт',11:'ноя',12:'дек'}
dict_dates_full = {1:'января',2:'февраля',3:'марта',4:'апреля',5:'мая',6:'июня',7:'июля',8:'августа',9:'сентября',10:'октября',11:'ноября',12:'декабря'}

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
day_prices = dbc.Card([dcc.Graph(id='my-graph1')])
hour_prices = dbc.Card([dcc.Graph(id='my-graph2'),dbc.CardBody(slider)])
date_for_table_1 = df_st_m.index[-1]
date_for_table_2 = df_st_m.index[-2]
table =dbc.Card([dcc.Graph(id='my-table',config={'displayModeBar': True,'scrollZoom':False,'staticPlot':True})])
collapse = html.Div(
    [
        dbc.Button(
            "Изменение цены",
            id="collapse-button",
            className="d-grid gap-2",
            color="primary",
            n_clicks=0, style = {'width':'100%'}
        ),
        dbc.Collapse(
            dbc.Card(table),
            id="collapse",
            is_open=False,
        ),
    ]
)

cards = html.Div(
    [
        dbc.Card(
            dbc.CardBody(day_prices),
            className="mb-3",style={'min-width':'600px'}),
        dbc.Card(dbc.CardBody(collapse),
            className="mb-3",style={'min-width':'600px'}),
        dbc.Card(dbc.CardBody(hour_prices),
            className="mb-3",style={'min-width':'600px'})
    ]
)

def App():
    layout = html.Div([nav,dropdown,cards],style={'background-color': '#D0DBEA','min-width':'600px'})
    return layout

