import pandas as pd
import requests
from bs4 import BeautifulSoup

Pass_Types = 'https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/passing_types/Manchester-City-Match-Logs-Premier-League'
response_pt = requests.get(Pass_Types)
soup_pt = BeautifulSoup(response_pt.text, 'html.parser')
table_pt = soup_pt.find('table')
df_pt = pd.read_html(str(table_pt), skiprows= 1)[0]
df_pt1 = df_pt.drop(df_pt.columns[[0,1,2,3,4,5,6,7,8,24]],axis=1)

print('Pass Type Dataframe created')