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
# from .datasets import df_st
from .start_page_companies import modal_ogk_card as modal_ogk,modal_tgk_card as modal_tgk,modal_mos_card as modal_mos,ogk_df,tgk_df,mos_df
df_ogk_m = ogk_df.resample('1D').mean()
df_tgk_m = tgk_df.resample('1D').mean()
df_mos_m = mos_df.resample('1D').mean()
date_for_table_1 = df_ogk_m.index[-1]
date_for_table_2 = df_ogk_m.index[-2]
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


dict_dates = {1:'янв',2:'фев',3:'мар',4:'апр',5:'мая',6:'июн',7:'июл',8:'авг',9:'сен',10:'окт',11:'ноя',12:'дек'}
dict_dates_full = {1:'января',2:'февраля',3:'марта',4:'апреля',5:'мая',6:'июня',7:'июля',8:'августа',9:'сентября',10:'октября',11:'ноября',12:'декабря'}




locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
modal = html.Div(className='plotly_body',children=[
    dbc.CardGroup([
modal_ogk,
modal_tgk,
modal_mos
        # dbc.Col(modal_ogk,width=3),
        # dbc.Col(modal_tgk,width=3),
        # dbc.Col(modal_mos,width=3)
                    ])
                 ]# style={'background-color':'red','height':'500px'}
)
app = DjangoDash('SimpleExample',add_bootstrap_links=True)
app.css.append_css({ "external_url" : "/static/dash_RSV/css/main.css" })
app.layout = modal

@app.callback(
    Output("modal-mos", "is_open"),
    Input("open-mos", "n_clicks"),
    State("modal-mos", "is_open"),
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open
@app.callback(Output("collapse-mos", "is_open"),
    [Input("collapse-button-mos", "n_clicks")],[State("collapse-mos", "is_open")],)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
@app.callback(
    Output("modal-tgk", "is_open"),
    Input("open-tgk", "n_clicks"),
    State("modal-tgk", "is_open"),
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open
@app.callback(Output("collapse-tgk", "is_open"),
    [Input("collapse-button-tgk", "n_clicks")],[State("collapse-tgk", "is_open")],)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
@app.callback(
    Output("modal-ogk", "is_open"),
    Input("open-ogk", "n_clicks"),
    State("modal-ogk", "is_open"),
)
def toggle_modal(n, is_open):
    if n:
        return not is_open
    return is_open
@app.callback(Output("collapse-ogk", "is_open"),
    [Input("collapse-button-ogk", "n_clicks")],[State("collapse-ogk", "is_open")],)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open
# # график для прогноза цен
@app.callback([Output('my-graph1-ogk', 'figure'),Output('my-graph2-ogk', 'figure'),Output('my-table-ogk', 'figure')],
              [Input('ogk-dropdown', 'value'),Input('date-slider-ogk', 'value')])
def update_graph(tab,date):
    figure = px.line(
                 ogk_df[tab].resample('1D').mean(),
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
        # rangeslider_visible=True,
        showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3'
        )
    figure.update_yaxes(showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3')
    df_ogk_d = pd.DataFrame(ogk_df[tab].resample('1D').mean())
    df_ogk_d['weekday']=df_ogk_d.index.weekday
    holidays=df_ogk_d[df_ogk_d['weekday'].isin([5,6])].index
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
            for elem in df_ogk_m.index]
    figure.update_xaxes(tickformat='%d-%b')
    figure.update_xaxes(tickvals=df_ogk_m.index)
    figure.update_xaxes(ticktext=ticktext)
    date_for_slider = df_ogk_m.index[date]
    y=date_for_slider.year
    m=date_for_slider.month
    d=date_for_slider.day
    df_ogk_h = ogk_df[(ogk_df.index.year==y)&(ogk_df.index.month==m)&(ogk_df.index.day==d)]
    figure_2 = px.line(
                df_ogk_h[tab],
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
    df_for_table = pd.DataFrame(df_ogk_m[tab])
    for tab in df_for_table.columns:
        for_table.append([tab,np.round(df_for_table[tab].iloc[-2]),np.round(df_for_table[tab].iloc[-1]),np.round(100*(df_for_table[tab].iloc[-1]-df_for_table[tab].iloc[-2])/df_for_table[tab].iloc[-2],2)])

    table_figure = ff.create_table(for_table)
    return figure,figure_2,table_figure

@app.callback([Output('my-graph1-tgk', 'figure'),Output('my-graph2-tgk', 'figure'),Output('my-table-tgk', 'figure')],
              [Input('tgk-dropdown', 'value'),Input('date-slider-tgk', 'value')])
def update_graph(tab,date):
    figure = px.line(
                 tgk_df[tab].resample('1D').mean(),
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
        # rangeslider_visible=True,
        showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3'
        )
    figure.update_yaxes(showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3')
    df_tgk_d = pd.DataFrame(tgk_df[tab].resample('1D').mean())
    df_tgk_d['weekday']=df_tgk_d.index.weekday
    holidays=df_tgk_d[df_tgk_d['weekday'].isin([5,6])].index
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
            for elem in df_tgk_m.index]
    figure.update_xaxes(tickformat='%d-%b')
    figure.update_xaxes(tickvals=df_tgk_m.index)
    figure.update_xaxes(ticktext=ticktext)
    date_for_slider = df_tgk_m.index[date]
    y=date_for_slider.year
    m=date_for_slider.month
    d=date_for_slider.day
    df_tgk_h = tgk_df[(tgk_df.index.year==y)&(tgk_df.index.month==m)&(tgk_df.index.day==d)]
    figure_2 = px.line(
                df_tgk_h[tab],
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
    df_for_table = pd.DataFrame(df_tgk_m[tab])
    for tab in df_for_table.columns:
        for_table.append([tab,np.round(df_for_table[tab].iloc[-2]),np.round(df_for_table[tab].iloc[-1]),np.round(100*(df_for_table[tab].iloc[-1]-df_for_table[tab].iloc[-2])/df_for_table[tab].iloc[-2],2)])

    table_figure = ff.create_table(for_table)
    return figure,figure_2,table_figure

@app.callback([Output('my-graph1-mos', 'figure'),Output('my-graph2-mos', 'figure'),Output('my-table-mos', 'figure')],
              [Input('mos-dropdown', 'value'),Input('date-slider-mos', 'value')])
def update_graph(tab,date):
    figure = px.line(
                 mos_df[tab].resample('1D').mean(),
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
        # rangeslider_visible=True,
        showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3'
        )
    figure.update_yaxes(showgrid=True,showline=True, linewidth=0.1, linecolor='black', gridcolor='#DDE6F3')
    df_mos_d = pd.DataFrame(mos_df[tab].resample('1D').mean())
    df_mos_d['weekday']=df_mos_d.index.weekday
    holidays=df_mos_d[df_mos_d['weekday'].isin([5,6])].index
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
            for elem in df_mos_m.index]
    figure.update_xaxes(tickformat='%d-%b')
    figure.update_xaxes(tickvals=df_mos_m.index)
    figure.update_xaxes(ticktext=ticktext)
    date_for_slider = df_mos_m.index[date]
    y=date_for_slider.year
    m=date_for_slider.month
    d=date_for_slider.day
    df_mos_h = mos_df[(mos_df.index.year==y)&(mos_df.index.month==m)&(mos_df.index.day==d)]
    figure_2 = px.line(
                df_mos_h[tab],
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
    df_for_table = pd.DataFrame(df_mos_m[tab])
    for tab in df_for_table.columns:
        for_table.append([tab,np.round(df_for_table[tab].iloc[-2]),np.round(df_for_table[tab].iloc[-1]),np.round(100*(df_for_table[tab].iloc[-1]-df_for_table[tab].iloc[-2])/df_for_table[tab].iloc[-2],2)])

    table_figure = ff.create_table(for_table)
    return figure,figure_2,table_figure







