import sqlalchemy as sa
import datetime
engine = sa.create_engine('sqlite:///consum.sqlite3')
connection=engine.connect()
# result = engine.execute("""
#         CREATE TABLE "generation_types" (
#            station_type TEXT,
#            generation FLOAT,
#            date DATETIME,
#            PRIMARY KEY (station_type,date)
#         )
#          """)

#удаляем данные старше 30 дней
date_for_clear = datetime.datetime.now().date() - datetime.timedelta(days=30)

# result = engine.execute("""
#         DELETE
#         FROM [generation_types]
#         WHERE date <= '{} 00:00:00.000000'
#          """.format(date_for_clear))


download_data=False
import requests
from bs4 import BeautifulSoup
import pandas as pd
import xlrd
import io
import datetime
import warnings
warnings.filterwarnings("ignore")
import time
import numpy as np
total_df = pd.DataFrame()

command=("""
SELECT *
FROM [generation_types]
""")

df = pd.read_sql_query(command,connection)
end_date = pd.to_datetime(df['date'].iloc[-1])
tommorow=datetime.datetime.now().date()+datetime.timedelta(days=1)
if download_data:
    days_list = pd.date_range(start=end_date,end=tommorow,freq='1D')
    for today in days_list:
        print(today)
        def date_fill(row):
            return pd.to_datetime(datetime.datetime(year=today.year, month=today.month, day=today.day, hour=row['hour']))

        y = today.year
        m = today.month
        d = today.day

        if m < 10: m = '0' + str(m)
        if d < 10: d = '0' + str(d)
        excel_href = ''
        url = 'https://www.atsenergo.ru/nreport?rname=trade_zone&region=eur&rdate=2022{}{}'.format(m, d)
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

        df = pd.io.excel.read_excel(fh,header=6,index_col=0)
        df_melt = pd.melt(df.reset_index(),id_vars='index')
        df_melt.columns=['hour','station_type','generation']
        df_melt['date']= df_melt.apply(date_fill,axis=1)
        total_df=pd.concat([total_df,df_melt])
    total_df.drop(columns='hour',inplace=True)

    total_df.to_sql('generation_types', con=connection, index=False, if_exists='append')

command=("""
SELECT *
FROM [generation_types]
""")

df = pd.read_sql_query(command,connection)


