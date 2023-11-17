import pandas as pd
import requests
from bs4 import BeautifulSoup

Defensive_Actions = 'https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/defense/Manchester-City-Match-Logs-Premier-League'
response_da = requests.get(Defensive_Actions)
soup_da = BeautifulSoup(response_da.text, 'html.parser')
table_da = soup_da.find('table')
df_da = pd.read_html(str(table_da), skiprows= 1)[0]
df_da1 = df_da.drop(df_da.columns[[0,1,2,3,4,5,6,7,8,25]], axis=1)

print('Defensive Actions Dataframe created')