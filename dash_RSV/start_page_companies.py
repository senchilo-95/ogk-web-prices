import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import locale
from .all_companies_data import ogk_df,tgk_df,mos_df

dict_dates = {1:'янв',2:'фев',3:'мар',4:'апр',5:'мая',6:'июн',7:'июл',8:'авг',9:'сен',10:'окт',11:'ноя',12:'дек'}
dict_dates_full = {1:'января',2:'февраля',3:'марта',4:'апреля',5:'мая',6:'июня',7:'июля',8:'августа',9:'сентября',10:'октября',11:'ноября',12:'декабря'}
range_of_dates=pd.date_range(start=ogk_df.index[0].date(),end=ogk_df.index[-1].date(),freq='1D')
dates_list = ['{} {}'.format(idx.day,dict_dates[idx.month]) for idx in range_of_dates]
df_ogk_m = ogk_df.resample('1D').mean()
df_tgk_m = tgk_df.resample('1D').mean()
df_mos_m = mos_df.resample('1D').mean()
#ОГК-2
slider_ogk=dcc.Slider(len(df_ogk_m)-14, len(df_ogk_m)-1,1, value=len(df_ogk_m)-1,
    marks={idx:'{} {}'.format(df_ogk_m.index[idx].day,dict_dates[df_ogk_m.index[idx].month]) for idx in range(len(df_ogk_m)-14,len(df_ogk_m))},
    included=False,
    id='date-slider-ogk'
)
slider_ogk = html.Div([slider_ogk], style={'height': '50px'})

day_prices_ogk = dbc.Card([dcc.Graph(id='my-graph1-ogk')])
hour_prices_ogk = dbc.Card([dcc.Graph(id='my-graph2-ogk'),dbc.CardBody(slider_ogk)])
# date_for_table_ogk_1 = df_ogk_m.index[-1]
# date_for_table_ogk_2 = df_ogk_m.index[-2]
table_ogk =dbc.Card([dcc.Graph(id='my-table-ogk',config={'displayModeBar': True,'scrollZoom':False,'staticPlot':True})])
collapse_ogk = html.Div(
    [
        dbc.Button(
            "Изменение цены",
            id="collapse-button-ogk",
            className="d-grid gap-2",
            color="primary",
            n_clicks=0, style = {'width':'100%'}
        ),
        dbc.Collapse(
            dbc.Card(table_ogk),
            id="collapse-ogk",
            is_open=False,
        ),
    ]
)

cards_ogk = html.Div(
    [
        dbc.Card(
            dbc.CardBody(day_prices_ogk),
            className="mb-3",style={'min-width':'600px'}),
        dbc.Card(dbc.CardBody(collapse_ogk),
            className="mb-3",style={'min-width':'600px'}),
        dbc.Card(dbc.CardBody(hour_prices_ogk),
            className="mb-3",style={'min-width':'600px'})
    ]
)

dropdown_ogk = dcc.Dropdown(
    id = 'ogk-dropdown',
    searchable=False,
    value='Киришская ГРЭС',
    options=[
{'label' : 'Все станции', 'value' : ogk_df.columns},
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
modal_ogk = html.Div(
    [
        dbc.Button("ПАО 'ОГК-2'", id="open-ogk"),
        dbc.Modal(
            [
                dbc.ModalHeader("ПАО 'ОГК-2'",),
                dbc.ModalBody(html.Div([dropdown_ogk,cards_ogk],style={'background-color': '#D0DBEA','min-width':'600px'})),
            ],
            id="modal-ogk",
            style={"max-width": "none", "width": "100%"},
            size="xxl",
            centered=False
        ),
    ],style={"margin": '50px','textAlign': 'center'}
                )

# ТГК-1
slider_tgk=dcc.Slider(len(df_tgk_m)-14, len(df_tgk_m)-1,1, value=len(df_tgk_m)-1,
    marks={idx:'{} {}'.format(df_tgk_m.index[idx].day,dict_dates[df_tgk_m.index[idx].month]) for idx in range(len(df_tgk_m)-14,len(df_tgk_m))},
    included=False,
    id='date-slider-tgk'
)
slider_tgk = html.Div([slider_tgk], style={'height': '50px'})

day_prices_tgk = dbc.Card([dcc.Graph(id='my-graph1-tgk')])
hour_prices_tgk = dbc.Card([dcc.Graph(id='my-graph2-tgk'),dbc.CardBody(slider_tgk)])
date_for_table_1 = df_ogk_m.index[-1]
date_for_table_2 = df_ogk_m.index[-2]
table_tgk =dbc.Card([dcc.Graph(id='my-table-tgk',config={'displayModeBar': True,'scrollZoom':False,'staticPlot':True})])
collapse_tgk = html.Div(
    [
        dbc.Button(
            "Изменение цены",
            id="collapse-button-tgk",
            className="d-grid gap-2",
            color="primary",
            n_clicks=0, style = {'width':'100%'}
        ),
        dbc.Collapse(
            dbc.Card(table_tgk),
            id="collapse-tgk",
            is_open=False,
        ),
    ]
)

cards_tgk = html.Div(
    [
        dbc.Card(
            dbc.CardBody(day_prices_tgk),
            className="mb-3",style={'min-width':'600px'}),
        dbc.Card(dbc.CardBody(collapse_tgk),
            className="mb-3",style={'min-width':'600px'}),
        dbc.Card(dbc.CardBody(hour_prices_tgk),
            className="mb-3",style={'min-width':'600px'})
    ]
)

dropdown_tgk = dcc.Dropdown(
    id = 'tgk-dropdown',
    searchable=False,
    value='Автовская ТЭЦ',
    options=[{'label': 'Все станции', 'value':tgk_df.columns},
             {'label': 'Автовская ТЭЦ', 'value': 'Автовская ТЭЦ'},
 {'label': 'Апатитская ТЭЦ', 'value': 'Апатитская ТЭЦ'},
 {'label': 'Беломорская ГЭС-6', 'value': 'Беломорская ГЭС-6'},
 {'label': 'Борисоглебская ГЭС', 'value': 'Борисоглебская ГЭС'},
 {'label': 'Василеостровская ТЭЦ', 'value': 'Василеостровская ТЭЦ'},
 {'label': 'Верхне-Свирская ГЭС', 'value': 'Верхне-Свирская ГЭС'},
 {'label': 'Верхне-Териберская ГЭС', 'value': 'Верхне-Териберская ГЭС'},
 {'label': 'Верхне-Туломская ГЭС-12', 'value': 'Верхне-Туломская ГЭС-12'},
 {'label': 'Волховская ГЭС', 'value': 'Волховская ГЭС'},
 {'label': 'Выборгская ТЭЦ', 'value': 'Выборгская ТЭЦ'},
 {'label': 'Выгостровская ГЭС-5', 'value': 'Выгостровская ГЭС-5'},
 {'label': 'Иовская ГЭС', 'value': 'Иовская ГЭС'},
 {'label': 'Кайтакоски ГЭС', 'value': 'Кайтакоски ГЭС'},
 {'label': 'Княжегубская ГЭС-11', 'value': 'Княжегубская ГЭС-11'},
 {'label': 'Кондопожская ГЭС-1', 'value': 'Кондопожская ГЭС-1'},
 {'label': 'Кривопорожская ГЭС-14', 'value': 'Кривопорожская ГЭС-14'},
 {'label': 'Кумская ГЭС', 'value': 'Кумская ГЭС'},
 {'label': 'Лесогорская ГЭС', 'value': 'Лесогорская ГЭС'},
 {'label': 'Маткожненская ГЭС-3', 'value': 'Маткожненская ГЭС-3'},
 {'label': 'Нарвская ГЭС', 'value': 'Нарвская ГЭС'},
 {'label': 'Нива ГЭС-2', 'value': 'Нива ГЭС-2'},
 {'label': 'Нива ГЭС-3', 'value': 'Нива ГЭС-3'},
 {'label': 'Нижне-Свирская ГЭС', 'value': 'Нижне-Свирская ГЭС'},
 {'label': 'Нижне-Туломская ГЭС-13', 'value': 'Нижне-Туломская ГЭС-13'},
 {'label': 'Палакагорская ГЭС-7', 'value': 'Палакагорская ГЭС-7'},
 {'label': 'Пальеозерская ГЭС-2', 'value': 'Пальеозерская ГЭС-2'},
 {'label': 'Первомайская ТЭЦ', 'value': 'Первомайская ТЭЦ'},
 {'label': 'Петрозаводская ТЭЦ', 'value': 'Петрозаводская ТЭЦ'},
 {'label': 'Подужемская ГЭС-10', 'value': 'Подужемская ГЭС-10'},
 {'label': 'Правобережная ТЭЦ', 'value': 'Правобережная ТЭЦ'},
 {'label': 'Путкинская ГЭС-9', 'value': 'Путкинская ГЭС-9'},
 {'label': 'Раякоски ГЭС', 'value': 'Раякоски ГЭС'},
 {'label': 'Светогорская ГЭС', 'value': 'Светогорская ГЭС'},
 {'label': 'Северная ТЭЦ', 'value': 'Северная ТЭЦ'},
 {'label': 'Серебрянская ГЭС-1', 'value': 'Серебрянская ГЭС-1'},
 {'label': 'Серебрянская ГЭС-2', 'value': 'Серебрянская ГЭС-2'},
 {'label': 'Хевоскоски ГЭС', 'value': 'Хевоскоски ГЭС'},
 {'label': 'ЭС-1 Центральной ТЭЦ (Г-1)',
  'value': 'ЭС-1 Центральной ТЭЦ (Г-1)'},
 {'label': 'Южная ТЭЦ', 'value': 'Южная ТЭЦ'},
 {'label': 'Янискоски ГЭС', 'value': 'Янискоски ГЭС'}],style={'width':'400px', 'align-items': 'center', 'justify-content': 'center'}
)
modal_tgk = html.Div(
    [
        dbc.Button("ПАО 'ТГК-1'", id="open-tgk"),
        dbc.Modal(
            [
                dbc.ModalHeader("ПАО 'ТГК-1'",),
                dbc.ModalBody(html.Div([dropdown_tgk,cards_tgk],style={'background-color': '#D0DBEA','min-width':'600px'})),
            ],
            id="modal-tgk",
            style={"max-width": "none", "width": "100%"},
            size="xxl",
            centered=False
        ),
    ],style={"margin": '50px','textAlign': 'center'}
                )

# ПАО "Мосэнерго"
slider_mos=dcc.Slider(len(df_mos_m)-14, len(df_mos_m)-1,1, value=len(df_mos_m)-1,
    marks={idx:'{} {}'.format(df_mos_m.index[idx].day,dict_dates[df_mos_m.index[idx].month]) for idx in range(len(df_mos_m)-14,len(df_mos_m))},
    included=False,
    id='date-slider-mos'
)
slider_mos = html.Div([slider_mos], style={'height': '50px'})
day_prices_mos = dbc.Card([dcc.Graph(id='my-graph1-mos')])
hour_prices_mos = dbc.Card([dcc.Graph(id='my-graph2-mos'),dbc.CardBody(slider_mos)])
# date_for_table_ogk_1 = df_ogk_m.index[-1]
# date_for_table_ogk_2 = df_ogk_m.index[-2]
table_mos =dbc.Card([dcc.Graph(id='my-table-mos',config={'displayModeBar': True,'scrollZoom':False,'staticPlot':True})])
collapse_mos = html.Div(
    [
        dbc.Button(
            "Изменение цены",
            id="collapse-button-mos",
            className="d-grid gap-2",
            color="primary",
            n_clicks=0, style = {'width':'100%'}
        ),
        dbc.Collapse(
            dbc.Card(table_mos),
            id="collapse-mos",
            is_open=False,
        ),
    ]
)

cards_mos = html.Div(
    [
        dbc.Card(
            dbc.CardBody(day_prices_mos),
            className="mb-3",style={'min-width':'600px'}),
        dbc.Card(dbc.CardBody(collapse_mos),
            className="mb-3",style={'min-width':'600px'}),
        dbc.Card(dbc.CardBody(hour_prices_mos),
            className="mb-3",style={'min-width':'600px'})
    ]
)

dropdown_mos = dcc.Dropdown(
    id = 'mos-dropdown',
    searchable=False,
    value='ТЭЦ-11',
    options=[
        {'label':'Все станции','value':mos_df.columns},
         {'label': 'Б/ст ТЭЦ Московского КГЗ', 'value': 'Б/ст ТЭЦ Московского КГЗ'},
 {'label': 'ГРЭС-3', 'value': 'ГРЭС-3'},
 {'label': 'ГЭС-1', 'value': 'ГЭС-1'},
 {'label': 'ТЭЦ-11', 'value': 'ТЭЦ-11'},
 {'label': 'ТЭЦ-12', 'value': 'ТЭЦ-12'},
 {'label': 'ТЭЦ-16', 'value': 'ТЭЦ-16'},
 {'label': 'ТЭЦ-17', 'value': 'ТЭЦ-17'},
 {'label': 'ТЭЦ-20', 'value': 'ТЭЦ-20'},
 {'label': 'ТЭЦ-21', 'value': 'ТЭЦ-21'},
 {'label': 'ТЭЦ-22', 'value': 'ТЭЦ-22'},
 {'label': 'ТЭЦ-23', 'value': 'ТЭЦ-23'},
 {'label': 'ТЭЦ-25', 'value': 'ТЭЦ-25'},
 {'label': 'ТЭЦ-26', 'value': 'ТЭЦ-26'},
 {'label': 'ТЭЦ-27', 'value': 'ТЭЦ-27'},
 {'label': 'ТЭЦ-30', 'value': 'ТЭЦ-30'},
 {'label': 'ТЭЦ-8', 'value': 'ТЭЦ-8'},
 {'label': 'ТЭЦ-9', 'value': 'ТЭЦ-9'}],style={'width':'400px', 'align-items': 'center', 'justify-content': 'center'}
)
modal_mos = html.Div(
    [
        dbc.Button("ПАО 'Мосэнерго'", id="open-mos"),
        dbc.Modal(
            [
                dbc.ModalHeader("ПАО 'Мосэнерго'",),
                dbc.ModalBody(html.Div([dropdown_mos,cards_mos],style={'background-color': '#D0DBEA','min-width':'600px'})),
            ],
            id="modal-mos",
            style={"max-width": "none", "width": "100%"},
            size="xxl",
            centered=False
        ),
    ],style={"margin": '50px','textAlign': 'center'}
                )
