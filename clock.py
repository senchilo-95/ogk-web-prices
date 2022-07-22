from apscheduler.schedulers.blocking import BlockingScheduler
import sqlalchemy as sa
import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlrd
import io
import datetime
import time

sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=3)
# def timed_job():
#     print('This job is run every three minutes.')

@sched.scheduled_job('cron',hour=14, minute=40)
def scheduled_job():
    dict_stations ={
    'Череповецкая ГРЭС':529874,
    'Адлерская ТЭС':[300347,300323],
    'Грозненская ТЭС':300691,
    'Псковская ГРЭС':405201,
    'Рязанская ГРЭС':[531962,531961],
    'Новочеркасская ГРЭС':[300194,300195,300193],
    'Сургутская ГРЭС-1':[101170,101140],
    'Троицкая ГРЭС':[100154,100153],
    'Ставропольская ГРЭС':[300405,300404,300403,300402,300401],
    'Киришская ГРЭС':[403618,403633],
        'Серовская ГРЭС':[100077,100082]
    }
    stations = list(dict_stations.keys())

    engine = sa.create_engine('sqlite:///db.sqlite3')
    connection=engine.connect()

    command=("""
    SELECT date
    FROM [dash_RSV_prices_rsv_from_ats]
    ORDER BY date DESC
    """)

    dates = pd.read_sql_query(command,connection)
    dates['date']=pd.to_datetime(dates['date'])

    end_date=(pd.to_datetime(dates.iloc[0].values[0]).date())

    time_hour = datetime.datetime.now().hour

    tommorow = datetime.datetime.today()+datetime.timedelta(days=1)
    day_now=datetime.datetime.today()
    print('Дата в базе = {}, дата текущая = {} час = {}'.format(end_date,day_now.date(), time_hour))

    if (day_now.date()>end_date) or (tommorow.date()>end_date and time_hour>=17):
        date_end_for_range = tommorow.date()
        print(f'Загрузка данных с {end_date}')
        # try:
        range_dates=pd.date_range(start=end_date+datetime.timedelta(days=1),end=date_end_for_range)
        print(range_dates)
        for today in range_dates:
            # try:
            print(today)
            # try:
            y = today.year
            m=today.month
            d=today.day

            if m<10: m = '0'+str(m)
            if d<10: d = '0'+str(d)
            excel_href=''
            url = 'https://www.atsenergo.ru/nreport?rname=big_nodes_prices_pub&rdate=2022{}{}'.format(m,d)
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, 'lxml')
            for a in soup.find_all('a', href=True, title=True):
                if 'Заархивированный' in a['title']:

                    excel_href = a

            link_end = str(excel_href).split('"')[1]
            link_end.replace('amp;','')
            link = 'https://www.atsenergo.ru/nreport' + link_end
            print(link)
            time1 = time.time()
            r = requests.get(link, stream=True,verify=False)
            time2 = time.time()
            print('Запрос=', time2-time1)
            fh=io.BytesIO(r.content)

            test_dict={}

            for i in range(24):
                df = pd.io.excel.read_excel(fh,sheet_name=i,header=2,usecols=[0,5],index_col=0)
                time3= time.time()
                print(f'Час {i} Загрузка в файл', time3-time2)
                prices={}
                for st in stations:
                    prices[st]=float(df.loc[dict_stations[st]].mean())
                test_dict[i]=prices
            df_t=pd.DataFrame(test_dict).T
            def fill_date(row):
                return datetime.datetime(year=int(y),month=int(m),day=(d),hour=int(row['index']))
            df_t.reset_index(inplace=True)
            df_t['date']=df_t.apply(fill_date,axis=1)
            df_t=df_t.drop(columns='index')
            df_t=df_t.melt(id_vars='date',var_name='station')
            df_t.columns=['date','station','price']
            print(df_t)
            df_t.to_sql('dash_RSV_prices_rsv_from_ats', con=engine, index=True, index_label='id', if_exists='append')
            connection.close()

sched.start()
