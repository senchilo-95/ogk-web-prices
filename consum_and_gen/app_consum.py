
from django_plotly_dash import DjangoDash
import datetime
import dash_bootstrap_components as dbc
from .parser_so import consum_df
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import locale
import plotly.graph_objects as go
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
import pandas as pd



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

dropdown = dcc.Dropdown(
    id = 'oes-dropdown',
    searchable=False,
    value='ОЭС Юга',
    options=[
{'label' : 'ОЭС Юга', 'value' : 'ОЭС Юга'},
{'label' : 'ОЭС Северо-Запада', 'value' : 'ОЭС Северо-Запада'},
{'label' : 'ОЭС Центра', 'value' : 'ОЭС Центра'},
{'label' : 'ОЭС Урала', 'value' : 'ОЭС Урала'},
{'label' : 'ОЭС Средней Волги', 'value' : 'ОЭС Средней Волги'}
    ],style={'width':'400px', 'align-items': 'center', 'justify-content': 'center'}
)
consum_df['generation']=consum_df['generation'].astype('float')
consum_df['consumption']=consum_df['consumption'].astype('float')

consum_df_gen_h = pd.pivot_table(consum_df,index='date',columns='ups',values='consumption')
consum_df_cons_h = pd.pivot_table(consum_df,index='date',columns='ups',values='generation')

consum_df_gen_d = consum_df_gen_h.resample('1D').mean()
consum_df_cons_d = consum_df_cons_h.resample('1D').mean()

slider=dcc.Slider(len(consum_df_gen_d)-14, len(consum_df_gen_d)-1,1, value=len(consum_df_gen_d)-1,
    marks={idx:'{} {}'.format(consum_df_gen_d.index[idx].day,dict_dates[consum_df_gen_d.index[idx].month]) for idx in range(len(consum_df_gen_d)-14,len(consum_df_gen_d))},
    included=False,
    id='date_slider'
)
slider = html.Div([slider], style={'height': '50px'})
day_consum = dbc.Card([dcc.Graph(id='my-graph1',style = {'width':'98%'})])
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

app = DjangoDash('ConsumApp',add_bootstrap_links=True)
app.css.append_css({ "external_url" : "/static/dash_RSV/css/main.css" })
app.layout =  html.Div([dropdown,cards],style={'background-color': '#D0DBEA','min-width':'600px','width':'100%'})

@app.callback([Output('my-graph1', 'figure'),Output('my-graph2', 'figure')],
              [Input('oes-dropdown', 'value'),Input('date_slider', 'value')])
def update_graph(tab,date):
    figure = px.line(
                title="Среднесуточное потребление и генерация",
                labels={
               "date": "Дата. Выберите период.",
                 "value": "МВт*ч",
                    'variable':'ОЭС'
                    },
                template="plotly_white",markers=True)
    figure.update_xaxes(
        dtick="D",
        tickformat="%d%b",
        # rangeslider_visible=True,
        showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3'
        )
    figure.update_yaxes(showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3')


    ticktext=[datetime.datetime.strptime(str(elem.date()), "%Y-%m-%d").strftime('%d-%b')
            for elem in consum_df_gen_d.index]
    figure.update_xaxes(tickformat='%d-%b')
    figure.update_xaxes(tickvals=consum_df_gen_d.index)
    figure.update_xaxes(ticktext=ticktext)
    figure.update_xaxes(tickangle=90)
    figure.add_trace(go.Scatter(x=consum_df_cons_d.index, y=consum_df_cons_d[tab].values,
                             name='Потребление'))
    figure.add_trace(go.Scatter(x=consum_df_gen_d.index, y=consum_df_gen_d[tab].values,
                                name='Генерация'))

    consum_df_cons_d['weekday']=consum_df_cons_d.index.weekday
    holidays=consum_df_cons_d[consum_df_cons_d['weekday'].isin([5,6])].index
    delta = datetime.timedelta(minutes=60*12)
    for i in range(0,len(holidays),2):
        try:
            figure.add_vrect(x0=holidays[i]-delta, x1=holidays[i]+datetime.timedelta(days=2)-delta,
              annotation_text="Вых.", annotation_position="top left",
              fillcolor="#8DB1E1", opacity=0.2, line_width=0.1)
        except:
            figure.add_vrect(x0=holidays[i]-delta,x1=holidays[i]+datetime.timedelta(days=1)-delta,
                  annotation_text="Вых.", annotation_position="top left",
                  fillcolor="#8DB1E1", opacity=0.2, line_width=0.1)
    # figure.update_layout(width=1200)
    date_for_slider = consum_df_gen_d.index[date]
    y=date_for_slider.year
    m=date_for_slider.month
    d=date_for_slider.day
    consum_df_gen_now = consum_df_gen_h[(consum_df_gen_h.index.year==y)&(consum_df_gen_h.index.month==m)&(consum_df_gen_h.index.day==d)]
    consum_df_cons_now = consum_df_cons_h[(consum_df_cons_h.index.year==y)&(consum_df_cons_h.index.month==m)&(consum_df_cons_h.index.day==d)]

    figure.update_layout(height=400,showlegend=True)
    figure_2 = px.line(
        title="Почасовое потребление и генерация на " + "{} {}".format(d, dict_dates_full[m]),
        labels={
            "date": "Час суток",
            "value": "МВт*ч",
            'variable': 'ОЭС'
        }, template="plotly_white", markers=True)
    figure_2.add_trace(go.Scatter(x=consum_df_cons_now.index, y=consum_df_cons_now[tab].values,
                                name='Потребление'))
    figure_2.add_trace(go.Scatter(x=consum_df_gen_now.index, y=consum_df_gen_now[tab].values,
                                name='Генерация'))
    figure_2.update_xaxes(
        ticktext=[i for i in range(24)],
        showgrid=True, showline=True, linewidth=0.5, linecolor='black', gridcolor='#DDE6F3')
    figure_2.update_yaxes(showgrid=True, showline=True, linewidth=0.5, linecolor='black', gridcolor='#DDE6F3')
    figure_2.update_layout(height=400, showlegend=True)
    return figure,figure_2



