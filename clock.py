from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import io
import time
import numpy as np
import sqlalchemy as sa

engine = sa.create_engine('sqlite:///consum.sqlite3',connect_args={"check_same_thread": False}, echo=True)
download_data = True
connection = engine.connect()
dict_stations = {
    'Череповецкая ГРЭС': 529874,
    'Адлерская ТЭС': [300347, 300323],
    'Грозненская ТЭС': 300691,
    'Псковская ГРЭС': 405201,
    'Рязанская ГРЭС': [531962, 531961],
    'Новочеркасская ГРЭС': [300194, 300195, 300193],
    'Сургутская ГРЭС-1': [101170, 101140],
    'Троицкая ГРЭС': [100154, 100153],
    'Ставропольская ГРЭС': [300405, 300404, 300403, 300402, 300401],
    'Киришская ГРЭС': [403618, 403633],
    'Серовская ГРЭС': [100077, 100082]
}
stations = list(dict_stations.keys())
oes_dict = {'oes-northwest': 'ОЭС Северо-Запада', 'oes-ural': 'ОЭС Урала',
            'oes-volga': 'ОЭС Средней Волги', 'oes-south': 'ОЭС Юга',
            'oes-center': 'ОЭС Центра'}
oes_list = (list(oes_dict.keys()))


def power_datatable(url, oes, end_t):
    url = url
    response = requests.get(url, stream=True, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', {'class': 'big-chart'})
    items = str(items)
    index_start = items.find('data-datax="')
    index_end = items.find('" data-date="')
    data = items[index_start + len('data-datax="'):index_end]
    dates = data[:data.find('" data-datay="')]
    dates = (dates.split(','))
    dates = pd.to_datetime(dates)
    consum = data[data.find('data-datay="') + len('data-datay="'):data.find('" data-datay1="')]
    consum = consum.split(',')

    gen = data[data.find('" data-datay1="') + len('" data-datay1="'):]
    gen = gen.split(',')

    data_power = pd.DataFrame(index=dates, columns=['consum', 'gen'])
    data_power['consum'] = consum
    data_power['gen'] = (gen)
    data_power['oes'] = oes_dict[oes]
    data_power.reset_index(inplace=True)
    data_power.columns = ['date', 'generation', 'consumption', 'ups']
    data_power['date'] = pd.to_datetime(data_power['date'])
    data_power = data_power[data_power['date'] > pd.to_datetime(end_t)]
    return data_power


sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')


@sched.scheduled_job('cron', hour='14',minute='50')
def scheduled_job():
    try:
        command = ("""
         SELECT *
         FROM [generation_and_consumption]
         """)

        df = pd.read_sql_query(command, connection)
        end_time = (pd.to_datetime(df['date'].dropna().values[-1]))
        end_date = end_time.date()

        # connection.close()
        # result = engine.execute("""
        # CREATE TABLE "generation_and_consumption" (
        #    date DATETIME,
        #    generation FLOAT,
        #    consumption FLOAT,
        #    ups TEXT,
        #    PRIMARY KEY (date, ups)
        # )
        #  """)

        # sql = ('DROP TABLE generation_and_consumption;')
        # result = engine.execute(sql)
        start_date = pd.to_datetime(end_date).date()

        if datetime.datetime.now().hour >= 14:
            end_date_now = pd.to_datetime(datetime.datetime.now() + datetime.timedelta(days=1)).date()
        else:
            end_date_now = pd.to_datetime(datetime.datetime.now()).date()
        number_days = (end_date_now - start_date).days + 1
        dates = [(start_date + datetime.timedelta(days=i)) for i in range(number_days)]
        for oes in oes_list:
            urls = r'https://www.so-ups.ru/functioning/ees/{}/{}-indicators/{}-gen-consump-plan/?tx_mscdugraph_pi%5Bcontroller%5D=Graph&tx_mscdugraph_pi%5Baction%5D=fullview&tx_mscdugraph_pi%5BviewDate%5D={}'
            for url in dates:
                now1 = urls.format(oes, oes, oes, url)
                df1 = power_datatable(now1, oes, end_time)
                # time.sleep(5)
                # connection = engine.connect()
                df1.to_sql('generation_and_consumption', con=connection, index=False, if_exists='append')
                # connection.close()
    except:
        print('something wrong')
        pass

    command = ("""
    SELECT date
    FROM [dash_RSV_prices_rsv_from_ats]
    ORDER BY date DESC
    """)

    dates = pd.read_sql_query(command, connection)
    dates['date'] = pd.to_datetime(dates['date'])

    end_date = (pd.to_datetime(dates.iloc[0].values[0]).date())

    time_hour = datetime.datetime.now().hour

    tommorow = datetime.datetime.today() + datetime.timedelta(days=1)
    day_now = datetime.datetime.today()
    print('Дата в базе = {}, дата текущая = {} час = {}'.format(end_date, day_now.date(), time_hour))

    # if (day_now.date()>end_date) or (tommorow.date()>end_date and time_hour>=14):
    # try:
    date_end_for_range = tommorow.date()
    print(f'Загрузка данных с {end_date}')
    # try:
    range_dates = pd.date_range(start=end_date + datetime.timedelta(days=1), end=date_end_for_range)
    print(range_dates)
    data_df = pd.DataFrame()
    try:
        for today in range_dates:
            # try:
            # print(today)
            # try:
            y = today.year
            m = today.month
            d = today.day

            if m < 10: m = '0' + str(m)
            if d < 10: d = '0' + str(d)
            excel_href = ''
            url = 'https://www.atsenergo.ru/nreport?rname=big_nodes_prices_pub&rdate=2022{}{}'.format(m, d)
            response = requests.get(url, verify=False)
            soup = BeautifulSoup(response.text, 'lxml')
            #     prices = []
            for a in soup.find_all('a', href=True, title=True):
                if 'Заархивированный' in a['title']:
                    excel_href = a

            link_end = str(excel_href).split('"')[1]
            link_end.replace('amp;', '')
            link = 'https://www.atsenergo.ru/nreport' + link_end
            print(link)
            time1 = time.time()
            r = requests.get(link, stream=True, verify=False)
            time2 = time.time()
            print('Запрос=', time2 - time1)
            fh = io.BytesIO(r.content)

            test_dict = {}

            for i in range(24):
                df = pd.io.excel.read_excel(fh, sheet_name=i, header=2, usecols=[0, 5], index_col=0)
                time3 = time.time()
                print(f'Час {i} Загрузка в файл', np.round(time3 - time2), ' секунд')
                prices = {}
                for st in stations:
                    prices[st] = float(df.loc[dict_stations[st]].mean())
                test_dict[i] = prices
            df_t = pd.DataFrame(test_dict).T

            def fill_date(row):
                return datetime.datetime(year=int(y), month=int(m), day=int(d), hour=int(row['index']))

            df_t.reset_index(inplace=True)
            df_t['date'] = df_t.apply(fill_date, axis=1)
            df_t = df_t.drop(columns='index')
            df_t = df_t.melt(id_vars='date', var_name='station')
            df_t.columns = ['date', 'station', 'price']
            # data_df=pd.concat([data_df,df_t],axis=0)
            df_t.to_sql('dash_RSV_prices_rsv_from_ats', con=engine, index=True, index_label='id', if_exists='append')
    except:
        print('something wrong')
        pass
    print('good job')


# scheduled_job()
sched.start()
