import pandas as pd
import requests
from bs4 import BeautifulSoup

Passing = 'https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/passing/Manchester-City-Match-Logs-Premier-League'
response_pa = requests.get(Passing)
soup_pa = BeautifulSoup(response_pa.text, 'html.parser')
table_pa = soup_pa.find('table')
df_pa = pd.read_html(str(table_pa), skiprows= 1)[0]
df_pa1 = df_pa.drop(df_pa.columns[[0,1,2,3,4,5,6,7,8,31]],axis=1)

print('Passing Dataframe created')