import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

df= pd.read_csv('Masterlink.csv')

chunk_size= 8
total_rows= len(df)

for i in range(0,total_rows, chunk_size):
    chunk_dataframe= df.iloc[i:i + chunk_size]
    Sh= chunk_dataframe.iloc[0]
    Shooting= Sh.to_string(header=False,index=False)
    #print(Shooting)

    response_sh = requests.get(Shooting)

    soup_sh = BeautifulSoup(response_sh.text, 'html.parser')

    table_sh = soup_sh.find('table')

    df_sh = pd.read_html(str(table_sh), skiprows=1)[0]
    df_sh = df_sh.drop(df_sh.columns[[24]], axis=1)
    df_sh1 = df_sh.drop(df_sh.index[-1])


    filename= f'chunk_{i // chunk_size +1}.csv'
    Shooting.to_csv(filename, index=False)

    print(f"Chunk {i // chunk_size +1}:\n",chunk_dataframe)
    print("\n"+ "="*40 + "\n")



