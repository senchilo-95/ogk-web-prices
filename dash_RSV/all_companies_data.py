import sqlalchemy as sa
import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlrd
import io
import datetime
import time
import numpy as np
#
from sqlalchemy.orm import sessionmaker, scoped_session
# all_prices = pd.read_excel('dash_RSV/prices_all_comp.xlsx',engine='openpyxl',index_col=0)
# print(all_prices)
engine = sa.create_engine('sqlite:///consum.sqlite3')
connection=engine.connect()
# result = engine.execute("""
#         CREATE TABLE "prices_all" (
#            station TEXT,
#            price FLOAT,
#            gen_company TEXT,
#            date DATETIME,
#            PRIMARY KEY (station, gen_company,date)
#         )
#          """)
# all_prices.to_sql('prices_all', con=connection, index=False, if_exists='replace')


command=("""
SELECT date
FROM [prices_all]
""")

dates = pd.read_sql_query(command,connection)
end_date_db=(pd.to_datetime(dates.values[-1][0]).date())


# sql = ('DROP TABLE prices_all;')
# result = engine.execute(sql)


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
# #

gen_id_dict = np.load('dash_RSV/dict_1.npy',allow_pickle=True).item()
number_names_dict = np.load('dash_RSV/dict_2.npy',allow_pickle=True).item()

range_dates = pd.date_range(start=pd.to_datetime(end_date_db)+datetime.timedelta(days=1), end=pd.to_datetime(datetime.datetime.now().date())+datetime.timedelta(days=1))
all_comp_df = pd.DataFrame()
print(range_dates)

def number_to_station_name(row):
    number = row['Номер узла']
    try:
        return number_names_dict[number]
    except:
        return None
download_data=True
if download_data:
    try:
        for date in range_dates:
            if pd.to_datetime(end_date_db) <pd.to_datetime(date):
                print(date)
                today = date
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


                def date_fill(row):
                    return pd.to_datetime(datetime.datetime(year=date.year, month=date.month, day=date.day, hour=row['hour']))


                prices_hour = {h: [] for h in range(24)}
                for h in range(24):
                    prices_df = pd.io.excel.read_excel(fh, sheet_name=h, header=2, usecols=[0, 5])
                    #         prices_df = pd.read_excel('/Users/nikitasencilo/PycharmProjects/new_web_app/new-app-consum/dash_RSV/prices.xls', sheet_name=h, header=2, usecols=[0, 5])
                    prices_df['Номер узла'] = prices_df['Номер узла'].astype('str')
                    prices_df['name'] = prices_df.apply(number_to_station_name, axis=1)
                    prices_df.dropna(inplace=True)
                    for gen_comp in list(gen_id_dict.keys()):
                        #         print(gen_comp)
                        prices_hour_gen = {}
                        numbers = list(gen_id_dict[gen_comp])
                        prices_gen_comp = prices_df[prices_df['Номер узла'].isin(numbers)]
                        prices_gen_comp_dict = prices_gen_comp.groupby('name')['Цена, руб'].mean().to_dict()
                        prices_hour_gen[gen_comp] = prices_gen_comp_dict

                        prices_hour[h].append(prices_hour_gen)
                    print(h)

                gen_prices = {}
                all_companies = list(gen_id_dict.keys())

                for gen_name in all_companies:
                    g = all_companies.index(gen_name)
                    for h in range(24):
                        gen_prices[h] = prices_hour[h][g][gen_name]
                    gen_df = pd.DataFrame(gen_prices).T
                    gen_df_for_db = pd.melt(gen_df.reset_index(), id_vars='index',var_name='station', value_name='price')
                    gen_df_for_db.columns = ['hour', 'station', 'price']
                    gen_df_for_db['gen_company'] = gen_name
                    gen_df_for_db['date'] = gen_df_for_db.apply(date_fill, axis=1)
                    gen_df_for_db.drop(columns='hour', inplace=True)
                    all_comp_df = pd.concat([all_comp_df, gen_df_for_db])
                all_comp_df.to_sql('prices_all', con=connection, index=False, if_exists='append')
    except:
        print('Something Worng')
        pass
#

command=("""
SELECT *
FROM [prices_all]
""")

all_prices_df = pd.read_sql_query(command,connection)

all_prices_df['date'] = pd.to_datetime(all_prices_df['date'])
ogk_df=(pd.pivot_table(all_prices_df[all_prices_df['gen_company']=='ПАО "ОГК-2"'],index='date',columns='station',values='price'))
tgk_df=(pd.pivot_table(all_prices_df[all_prices_df['gen_company']=='ПАО "ТГК-1"'],index='date',columns='station',values='price'))
mos_df=(pd.pivot_table(all_prices_df[all_prices_df['gen_company']=='ПАО "Мосэнерго"'],index='date',columns='station',values='price'))
connection.close()

