import pandas as pd
from Shooting import df_sh1
from Goalkeeping import df_ke1
from Passing import df_pa1
from Passtype import df_pt1
from GCA import df_GCA1
from DefensiveActions import df_da1
from Posession import df_po1
from Misc import df_misc1

result = pd.concat([df_sh1, df_ke1, df_pa1, df_pt1, df_GCA1, df_da1, df_po1, df_misc1], axis=1, join="inner")

result.to_csv('table_data2.csv', index=False)

print('Table data has been scraped and saved as "table_data2.csv"')