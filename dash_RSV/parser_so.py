import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from sqlalchemy import create_engine
engine = create_engine('sqlite:///db.sqlite3', echo = True)
connection = engine.connect()
command=("""
SELECT *
FROM [generation_and_consumption]
""")

df = pd.read_sql_query(command,connection)
end_time=(pd.to_datetime(df['date'].dropna().values[-1]))
end_date = end_time.date()

# result=engine.execute("""
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


oes_dict={'oes-northwest':'ОЭС Северо-Запада','oes-ural':'ОЭС Урала',
          'oes-volga':'ОЭС Средней Волги','oes-south':'ОЭС Юга',
          'oes-center':'ОЭС Центра'}
oes_list = (list(oes_dict.keys()))

def power_datatable(url,oes):
    url = url
    response = requests.get(url, stream=True)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', {'class':'big-chart'})
    items=str(items)
    index_start = items.find('data-datax="')
    index_end = items.find('" data-date="')
    data = items[index_start+len('data-datax="'):index_end]
    dates = data[:data.find('" data-datay="')]
    dates = (dates.split(','))
    dates = pd.to_datetime(dates)
    consum = data[data.find('data-datay="')+len('data-datay="'):data.find('" data-datay1="')]
    consum = consum.split(',')

    gen = data[data.find('" data-datay1="')+len('" data-datay1="'):]
    gen = gen.split(',')

    data_power = pd.DataFrame(index=dates, columns = ['consum','gen'])
    data_power['consum'] = consum
    data_power['gen'] = (gen)
    data_power['oes'] = oes_dict[oes]
    data_power.reset_index(inplace=True)
    data_power.columns = ['date','generation','consumption','ups']
    data_power['date'] = pd.to_datetime(data_power['date'])
    data_power = data_power[data_power['date'] > pd.to_datetime(end_date)]
    return data_power

start_date = pd.to_datetime(end_date + datetime.timedelta(days=1)).date()
end_date_now = pd.to_datetime(datetime.datetime.now()).date()
number_days = (end_date_now-start_date).days + 1
dates = [(start_date + datetime.timedelta(days=i)) for i in range(number_days)]
for oes in oes_list:
    urls = r'https://www.so-ups.ru/functioning/ees/{}/{}-indicators/{}-gen-consump-hour/?tx_mscdugraph_pi%5Bcontroller%5D=Graph&tx_mscdugraph_pi%5Baction%5D=fullview&tx_mscdugraph_pi%5BviewDate%5D={}'
    for url in dates:
        now1 = urls.format(oes, oes, oes, url)
        df1 = power_datatable(now1, oes)
        time.sleep(5)
        df1.to_sql('generation_and_consumption', con=connection, index=False, if_exists='append')

command=("""
SELECT *
FROM [generation_and_consumption]
""")
connection = engine.connect()
consum_df = pd.read_sql_query(command,connection)
consum_df['date']=pd.to_datetime(consum_df['date'])
connection.close()

