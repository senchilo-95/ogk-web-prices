import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import datetime
import dash_bootstrap_components as dbc
from .navbar import Navbar
from .parser_so import consum_df
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import locale
nav = Navbar()
standard_BS = dbc.themes.BOOTSTRAP

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

app = Dash(__name__, external_stylesheets=[standard_BS])

dict_dates = {1:'янв',2:'фев',3:'мар',4:'апр',5:'мая',6:'июн',7:'июл',8:'авг',9:'сен',10:'окт',11:'ноя',12:'дек'}
dict_dates_full = {1:'января',2:'февраля',3:'марта',4:'апреля',5:'мая',6:'июня',7:'июля',8:'августа',9:'сентября',10:'октября',11:'ноября',12:'декабря'}

ues_tabs = dcc.Tabs(
    id="tabs-with-classes-consum",
    value='ОЭС Центра',
    parent_className='custom-tabs',
    className='custom-tabs-container',
    children=[
        dcc.Tab(
            label='ОЭС Центра',
            value='ОЭС Центра', className='custom-tab',
            selected_className='custom-tab--selected'
        ),
        dcc.Tab(
            label='ОЭС Юга',
            value='ОЭС Юга',
            className='custom-tab',
            selected_className='custom-tab--selected'
        ),
        dcc.Tab(
            label='ОЭС Северо-Запада',
            value='ОЭС Северо-Запада',
            className='custom-tab',
            selected_className='custom-tab--selected'
        ),
        dcc.Tab(
            label='ОЭС Урала',
            value='ОЭС Урала',
            className='custom-tab',
            selected_className='custom-tab--selected'
        ),
        dcc.Tab(
            label='ОЭС Средней Волги',
            value='ОЭС Средней Волги',
            className='custom-tab',
            selected_className='custom-tab--selected'
        )

    ])
consum_df_gen_h = pd.pivot_table(consum_df,index='date',columns='ups',values='generation')
consum_df_cons_h = pd.pivot_table(consum_df,index='date',columns='ups',values='generation')

consum_df_gen_d = consum_df_gen_h.resample('1D').mean()
consum_df_cons_d = consum_df_cons_h.resample('1D').mean()

slider=dcc.Slider(len(consum_df_gen_d)-14, len(consum_df_gen_d)-1,1, value=len(consum_df_gen_d)-1,
    marks={idx:'{} {}'.format(consum_df_gen_d.index[idx].day,dict_dates[consum_df_gen_d.index[idx].month]) for idx in range(len(consum_df_gen_d)-14,len(consum_df_gen_d))},
    included=False,
    id='date_slider'
)
slider = html.Div([slider], style={'height': '50px'})
day_consum = dbc.Card([dcc.Graph(id='my-graph1')])
hour_consum = dbc.Card([dcc.Graph(id='my-graph2'),dbc.CardBody(slider)])

cards = html.Div(
    [
        dbc.Card(
            dbc.CardBody(day_consum),
            className="mb-3",style={'min-width':'600px'}),
        dbc.Card(dbc.CardBody(hour_consum),
            className="mb-3",style={'min-width':'600px'})
    ]
)


def App_consum():
    layout =  html.Div([nav, ues_tabs,cards],style={'background-color': '#D0DBEA','min-width':'600px'})
    return layout


