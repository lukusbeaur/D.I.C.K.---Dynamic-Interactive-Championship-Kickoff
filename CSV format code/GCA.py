import pandas as pd
import requests
from bs4 import BeautifulSoup

GCA = 'https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/gca/Manchester-City-Match-Logs-Premier-League'
response_GCA = requests.get(GCA)
soup_GCA = BeautifulSoup(response_GCA.text, 'html.parser')
table_GCA = soup_GCA.find('table')
df_GCA = pd.read_html(str(table_GCA), skiprows= 1)[0]
df_GCA1 = df_GCA.drop(df_GCA.columns[[0,1,2,3,4,5,6,7,8,23]],axis=1)

print('GCA Dataframe created')