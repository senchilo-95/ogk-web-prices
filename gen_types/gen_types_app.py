from .gen_types_data import df

from django_plotly_dash import DjangoDash
import datetime
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import locale
import plotly.graph_objects as go
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
import pandas as pd
df['date']=pd.to_datetime(df['date'])
df_pivot = pd.pivot_table(df,index='date',columns='station_type',values='generation')
dict_dates = {1:'янв',2:'фев',3:'мар',4:'апр',5:'мая',6:'июн',7:'июл',8:'авг',9:'сен',10:'окт',11:'ноя',12:'дек'}
dict_dates_full = {1:'января',2:'февраля',3:'марта',4:'апреля',5:'мая',6:'июня',7:'июля',8:'августа',9:'сентября',10:'октября',11:'ноября',12:'декабря'}



gen_d = df_pivot.resample('1D').mean()
dropdown = dcc.Dropdown(
    id = 'gen-dropdown',
    searchable=False,
    value='ТЭС',
    options=[
{'label' : 'Все виды', 'value' : df_pivot.columns},
{'label' : 'ТЭС', 'value' : 'ТЭС'},
{'label' : 'АЭС', 'value' : 'АЭС'},
{'label' : 'ГЭС', 'value' : 'ГЭС'}
    ],style={'width':'400px', 'align-items': 'center', 'justify-content': 'center'}
)


slider=dcc.Slider(len(gen_d)-14, len(gen_d)-1,1, value=len(gen_d)-1,
    marks={idx:'{} {}'.format(gen_d.index[idx].day,dict_dates[gen_d.index[idx].month]) for idx in range(len(gen_d)-14,len(gen_d))},
    included=False,
    id='date_slider'
)
slider = html.Div([slider], style={'height': '50px'})
day_gen = dbc.Card([dcc.Graph(id='my-graph1')])
hour_gen = dbc.Card([dcc.Graph(id='my-graph2'),dbc.CardBody(slider)])

cards = html.Div(
    [
        dbc.Card(
            dbc.CardBody(day_gen),
            className="mb-3",style={'min-width':'600px'}),
        dbc.Card(dbc.CardBody(hour_gen),
            className="mb-3",style={'min-width':'600px'})
    ]
)

app_gen = DjangoDash('GenApp',add_bootstrap_links=True)
app_gen.css.append_css({ "external_url" : "/static/dash_RSV/css/main.css" })
app_gen.layout =  html.Div([dropdown,cards],style={'background-color': '#D0DBEA','min-width':'600px','width':'100%'})

@app_gen.callback([Output('my-graph1', 'figure'),Output('my-graph2', 'figure')],
              [Input('gen-dropdown', 'value'),Input('date_slider', 'value')])
def update_graph(tab,date):
    figure = px.line(gen_d.reset_index(),
                 x= 'date',
                 y= tab,
                title="Среднесуточная генерация по источникам",
                labels={
               "date": "Дата. Выберите период.",
                 "value": "МВт*ч",
                    'variable':'Источник'
                    },
                template="plotly_white",markers=True
                     )
    figure.update_xaxes(
        dtick="D",
        tickformat="%d%b",
        # rangeslider_visible=True,
        showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3'
        )
    figure.update_yaxes(showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3')


    # ticktext=[datetime.datetime.strptime(str(elem.date()), "%Y-%m-%d").strftime('%d-%b')
    #         for elem in gen_d.index]
    # figure.update_xaxes(tickformat='%d-%b')
    # figure.update_xaxes(tickvals=gen_d.index)
    # figure.update_xaxes(ticktext=ticktext)

    date_for_slider = gen_d.index[date]
    y=date_for_slider.year
    m=date_for_slider.month
    d=date_for_slider.day
    gen_now = df_pivot[(df_pivot.index.year==y)&(df_pivot.index.month==m)&(df_pivot.index.day==d)]

    figure.update_layout(height=400,showlegend=True)
    figure_2 = px.line(gen_now.reset_index(),
                 x= 'date',
                 y= tab,
        title="Почасовая генерация на " + "{} {}".format(d, dict_dates_full[m]),
        labels={
            "date": "Час суток",
            "value": "МВт*ч",
            'variable': 'Тип станции'
        },
                       template="plotly_white", markers=True
                       )
    figure_2.update_xaxes(
        ticktext=[i for i in range(24)],
        showgrid=True, showline=True, linewidth=0.5, linecolor='black', gridcolor='#DDE6F3')
    figure_2.update_yaxes(showgrid=True, showline=True, linewidth=0.5, linecolor='black', gridcolor='#DDE6F3')
    figure_2.update_layout(height=400, showlegend=True)
    return figure,figure_2




