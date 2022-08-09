import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
import datetime
import plotly.figure_factory as ff
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import locale
from .datasets import df_st
from .start_page_companies import modal_ogk
df_st_m = df_st.resample('1D').mean()
date_for_table_1 = df_st_m.index[-1]
date_for_table_2 = df_st_m.index[-2]
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


dict_dates = {1:'янв',2:'фев',3:'мар',4:'апр',5:'мая',6:'июн',7:'июл',8:'авг',9:'сен',10:'окт',11:'ноя',12:'дек'}
dict_dates_full = {1:'января',2:'февраля',3:'марта',4:'апреля',5:'мая',6:'июня',7:'июля',8:'августа',9:'сентября',10:'октября',11:'ноября',12:'декабря'}


modal_tgk = html.Div(
        [
            dbc.Button("ПАО 'ТГК-1'", id="open-tgk"),
            dbc.Modal(
                [
                    dbc.ModalHeader("ПАО 'ТГК-1'",),
                    dbc.ModalBody(html.Div([],style={'background-color': '#D0DBEA','min-width':'600px'})),
                ],
                id="modal-tgk",
                style={"max-width": "none", "width": "100%"},
                size="xxl",
                centered=False
            ),
        ],style={"margin": '50px','textAlign': 'center'}
                    )

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
modal = html.Div([modal_ogk,


])
app = DjangoDash('SimpleExample',add_bootstrap_links=True)
app.layout = modal

# @app.callback(
#     Output("modal-tgk", "is_open"),
#     Input("open-tgk", "n_clicks"),
#     State("modal-tgk", "is_open"),
# )
# def toggle_modal(n, is_open):
#     if n:
#         return not is_open
#     return is_open
@app.callback(
    Output("modal-ogk", "is_open"),
    Input("open-ogk", "n_clicks"),
    State("modal-ogk", "is_open"),
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open
@app.callback(Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],[State("collapse", "is_open")],)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
# # график для прогноза цен
@app.callback([Output('my-graph1-ogk', 'figure'),Output('my-graph2-ogk', 'figure'),Output('my-table-ogk', 'figure')],
              [Input('ogk-dropdown', 'value'),Input('date_slider', 'value')])
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






