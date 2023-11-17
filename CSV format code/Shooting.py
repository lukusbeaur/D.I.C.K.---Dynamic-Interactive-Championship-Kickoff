import pandas as pd
import requests
from bs4 import BeautifulSoup



Shooting = 'https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/shooting/Manchester-City-Match-Logs-Premier-League'

response_sh = requests.get(Shooting)

soup_sh = BeautifulSoup(response_sh.text, 'html.parser')

table_sh = soup_sh.find('table')

df_sh = pd.read_html(str(table_sh), skiprows= 1)[0]
df_sh = df_sh.drop(df_sh.columns[[24]], axis= 1)
df_sh1 = df_sh.drop(df_sh.index[-1])

print('Shooting Dataframe created')