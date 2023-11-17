import pandas as pd
import requests
from bs4 import BeautifulSoup

Possession = 'https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/possession/Manchester-City-Match-Logs-Premier-League'
response_po = requests.get(Possession)
soup_po = BeautifulSoup(response_po.text, 'html.parser')
table_po = soup_po.find('table')
df_po = pd.read_html(str(table_po), skiprows= 1)[0]
df_po1 = df_po.drop(df_po.columns[[0,1,2,3,4,5,6,7,8,32]], axis=1)

print('Posession Dataframe created')