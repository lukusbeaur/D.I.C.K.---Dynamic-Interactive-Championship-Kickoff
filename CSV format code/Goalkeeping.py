import pandas as pd
import requests
from bs4 import BeautifulSoup


Keeper = 'https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/keeper/Manchester-City-Match-Logs-Premier-League'
response_ke = requests.get(Keeper)
soup_ke = BeautifulSoup(response_ke.text, 'html.parser')
table_ke = soup_ke.find('table')
df_ke = pd.read_html(str(table_ke), skiprows= 1)[0]
df_ke1 = df_ke.drop(df_ke.columns[[0,1,2,3,4,5,6,7,8,35]],axis=1)

print('Goalkeeping Dataframe created')
