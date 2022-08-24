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
# engine = sa.create_engine('sqlite:///consum.sqlite3')
# connection=engine.connect()
# result = engine.execute("""
#         CREATE TABLE "generation_types" (
#            station_type TEXT,
#            generation FLOAT,
#            date DATETIME,
#            PRIMARY KEY (station_type,date)
#         )
#          """)