from dash import dash_table
import plotly.figure_factory as ff
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
# from dash import html, dcc
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
from django_plotly_dash import DjangoDash
import sqlalchemy as sa
from .datasets import df_st
import datetime
import plotly.figure_factory as ff
import locale
from .app_consum import App_consum, consum_df_gen_h,consum_df_gen_d,consum_df_cons_h,consum_df_cons_d
from .app import App


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

app = DjangoDash('SimpleExample',add_bootstrap_links=True)
app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

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

date_for_table_1 = df_st_m.index[-1]
date_for_table_2 = df_st_m.index[-2]

@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/app':
        return App()
    if pathname == '/app_consum':
        return App_consum()
    else:
        return App()
@app.callback(Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],[State("collapse", "is_open")],)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
# # график для прогноза цен
@app.callback([Output('my-graph1', 'figure'),Output('my-graph2', 'figure'),Output('my-table', 'figure')],
              [Input('station-dropdown', 'value'),Input('date_slider', 'value')])
def update_graph(tab,date):
    figure = px.line(
                 df_st[tab].resample('1D').mean(),
                title="Среднесуточные цены РСВ",
                labels={
               "date": "Дата. Выберите период.",
                 "value": "Цена РСВ, руб/МВт*ч",
                    'variable':'Станция'
                    },
                template="plotly_white",markers=True)
    figure.update_xaxes(
        dtick="D",
        tickformat="%d%b",
        rangeslider_visible=True,
        showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3'
        )
    figure.update_yaxes(showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3')
    df_st_d = pd.DataFrame(df_st[tab].resample('1D').mean())
    df_st_d['weekday']=df_st_d.index.weekday
    holidays=df_st_d[df_st_d['weekday'].isin([5,6])].index
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
    ticktext=[datetime.datetime.strptime(str(elem.date()), "%Y-%m-%d").strftime('%d-%b')
            for elem in df_st_m.index]
    figure.update_xaxes(tickformat='%d-%b')
    figure.update_xaxes(tickvals=df_st_m.index)
    figure.update_xaxes(ticktext=ticktext)
    date_for_slider = df_st_m.index[date]
    y=date_for_slider.year
    m=date_for_slider.month
    d=date_for_slider.day
    df_st_h = df_st[(df_st.index.year==y)&(df_st.index.month==m)&(df_st.index.day==d)]
    figure_2 = px.line(
                df_st_h[tab],
                title="Почасовые цены РСВ на "+"{} {}".format(d,dict_dates_full[m]),
                labels={
               "date": "Час суток",
                 "value": "Цена РСВ, руб/МВт*ч",
                    'variable':'Станция'
                    },template="plotly_white",markers=True)
    figure_2.update_xaxes(
        ticktext=[i for i in range(24)],
        showgrid=True,showline=True, linewidth=0.5, linecolor='black', gridcolor='#DDE6F3')
    figure_2.update_yaxes(showgrid=True,showline=True, linewidth=0.5, linecolor='black', gridcolor='#DDE6F3')

    figure.update_layout(height=400,showlegend=False)
    figure_2.update_layout(height=400,showlegend=False)

    for_table = [['Станция', '{} {}, руб./ МВт*ч'.format(date_for_table_2.day,dict_dates[date_for_table_2.month]),
                  '{} {}, руб./ МВт*ч'.format(date_for_table_1.day,dict_dates[date_for_table_1.month]),'Изменение цены, %']]
    df_for_table = pd.DataFrame(df_st_m[tab])
    for tab in df_for_table.columns:
        for_table.append([tab,np.round(df_for_table[tab].iloc[-2]),np.round(df_for_table[tab].iloc[-1]),np.round(100*(df_for_table[tab].iloc[-1]-df_for_table[tab].iloc[-2])/df_for_table[tab].iloc[-2],2)])

    table_figure = ff.create_table(for_table)
    return figure,figure_2,table_figure

@app.callback([Output('my-graph1', 'figure'),Output('my-graph2', 'figure')],
              [Input('tabs-with-classes-consum', 'value'),Input('date_slider', 'value')])
def update_graph(tab,date):
    figure = px.line(
                 consum_df_gen_d[tab],
                title="Среднесуточное потребление",
                labels={
               "date": "Дата. Выберите период.",
                 "value": "Потребление, МВт*ч",
                    'variable':'ОЭС'
                    },
                template="plotly_white",markers=True)
    figure.update_xaxes(
        dtick="D",
        tickformat="%d%b",
        rangeslider_visible=True,
        showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3'
        )
    figure.update_yaxes(showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3')


    ticktext=[datetime.datetime.strptime(str(elem.date()), "%Y-%m-%d").strftime('%d-%b')
            for elem in consum_df_gen_d.index]
    figure.update_xaxes(tickformat='%d-%b')
    figure.update_xaxes(tickvals=consum_df_gen_d.index)
    figure.update_xaxes(ticktext=ticktext)
    date_for_slider = consum_df_gen_d.index[date]
    y=date_for_slider.year
    m=date_for_slider.month
    d=date_for_slider.day
    consum_df_gen_now = consum_df_gen_h[(consum_df_gen_h.index.year==y)&(consum_df_gen_h.index.month==m)&(consum_df_gen_h.index.day==d)]

    figure.update_layout(height=400,showlegend=False)
    figure_2 = px.line(
        consum_df_gen_now[tab],
        title="Почасовое потребление на " + "{} {}".format(d, dict_dates_full[m]),
        labels={
            "date": "Час суток",
            "value": "Потребление, МВт*ч",
            'variable': 'ОЭС'
        }, template="plotly_white", markers=True)
    figure_2.update_xaxes(
        ticktext=[i for i in range(24)],
        showgrid=True, showline=True, linewidth=0.5, linecolor='black', gridcolor='#DDE6F3')
    figure_2.update_yaxes(showgrid=True, showline=True, linewidth=0.5, linecolor='black', gridcolor='#DDE6F3')
    figure_2.update_layout(height=400, showlegend=False)
    return figure,figure_2
