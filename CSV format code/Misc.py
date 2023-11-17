import pandas as pd
import requests
from bs4 import BeautifulSoup


Misc_stats = 'https://fbref.com/en/squads/b8fd03ef/2023-2024/matchlogs/c9/misc/Manchester-City-Match-Logs-Premier-League'
response_misc = requests.get(Misc_stats)
soup_misc = BeautifulSoup(response_misc.text, 'html.parser')
table_misc = soup_misc.find('table')
df_misc = pd.read_html(str(table_misc), skiprows= 1)[0]
df_misc1 = df_misc.drop(df_misc.columns[[0,1,2,3,4,5,6,7,8,25]], axis=1)

print('Misc Stats Dataframe created')