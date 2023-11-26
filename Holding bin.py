import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
from io import StringIO
import time


pd.set_option("display.max_colwidth",10000)

df= pd.read_csv('Masterlink2022-2023.csv') #Reads the CSV of mater links
chunk_size= 8 #There are 8 categories, therefore a chunk size of 8
total_rows= len(df) #Total amount of rows in the the master link

for i in range(0,total_rows, chunk_size):
    chunk_dataframe= df.iloc[i:i + chunk_size] #Iloc is used to pull rows from the dataframe, this is pulling 8 rows at a time i.e. the "Chunk size"

    Sh= chunk_dataframe.iloc[0]# This is creating a new dataframe of just the link for shooting so pulling a row of the chunk
    Gk= chunk_dataframe.iloc[1]
    Pa= chunk_dataframe.iloc[2]
    Pt= chunk_dataframe.iloc[3]
    Gs= chunk_dataframe.iloc[4]
    Da= chunk_dataframe.iloc[5]
    Po= chunk_dataframe.iloc[6]
    Mi= chunk_dataframe.iloc[7]


    Shooting= Sh.to_string(header=False, index=False) #Dataframe store their datatypes as objects, in order to parse the link using the request library the link needs to be a string so its not converting the object to a string
    Goalkeeping= Gk.to_string(header=False, index=False)
    Passing= Pa.to_string(header=False, index=False)
    Passtype= Pt.to_string(header=False, index=False)
    GCA= Gs.to_string(header=False, index=False)
    Defensiveaction= Da.to_string(header=False, index=False)
    Possession= Po.to_string(header=False, index=False)
    Misc= Mi.to_string(header=False, index=False)

    response_sh = requests.get(Shooting) # use request to pull up the webpage
    response_Gk = requests.get(Goalkeeping)
    response_Pa= requests.get(Passing)
    response_Pt= requests.get(Passtype)
    response_Gs= requests.get(GCA)
    response_Da= requests.get(Defensiveaction)
    response_Po= requests.get(Possession)
    response_Mi= requests.get(Misc)

    soup_sh = BeautifulSoup(response_sh.text, 'html.parser') #Use beautiful soup to parse the page into html

    soup_gk = BeautifulSoup(response_Gk.text, 'html.parser')
    soup_pa = BeautifulSoup(response_Pa.text, 'html.parser')
    soup_pt = BeautifulSoup(response_Pt.text, 'html.parser')
    soup_gs = BeautifulSoup(response_Gs.text, 'html.parser')
    soup_da = BeautifulSoup(response_Da.text, 'html.parser')
    soup_po = BeautifulSoup(response_Po.text, 'html.parser')
    soup_mi = BeautifulSoup(response_Mi.text, 'html.parser')

    table_sh = soup_sh.find('table') #Find the table in the page
    table_gk = soup_gk.find('table')
    table_pa = soup_pa.find('table')
    table_pt = soup_pt.find('table')
    table_gs = soup_gs.find('table')
    table_da = soup_da.find('table')
    table_po = soup_po.find('table')
    table_mi = soup_mi.find('table')

    #-----------------------------------------------Shooting Formatting-------------------------------------------
    df_sh = pd.read_html(str(table_sh), skiprows=1)[0] #Use pandas to read the html, and pull out the table skipping the header row
    df_sh = df_sh.drop(df_sh.columns[[24]], axis=1) #drop certain columns so that it can be formated corectly
    df_sh1 = df_sh.drop(df_sh.index[-1]) #again formating the table
    time.sleep(13)

    # -----------------------------------------------Goalkeeping Formatting-------------------------------------------
    df_ke = pd.read_html(str(table_gk), skiprows=1)[0]
    df_ke1 = df_ke.drop(df_ke.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 35]], axis=1)
    time.sleep(13)

    # -----------------------------------------------Passing Formatting-------------------------------------------
    df_pa = pd.read_html(str(table_pa), skiprows=1)[0]
    df_pa1 = df_pa.drop(df_pa.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 31]], axis=1)
    time.sleep(13)

    # -----------------------------------------------Passtype Formatting-------------------------------------------
    df_pt = pd.read_html(str(table_pt), skiprows=1)[0]
    df_pt1 = df_pt.drop(df_pt.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 24]], axis=1)
    time.sleep(13)

    # ----------------------------------------Goal and Shot creation Formatting---------------------------------------
    df_GCA = pd.read_html(str(table_gs), skiprows=1)[0]
    df_GCA1 = df_GCA.drop(df_GCA.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 23]], axis=1)
    time.sleep(13)

    # ----------------------------------------Defensive Actions Formatting---------------------------------------
    df_da = pd.read_html(str(table_da), skiprows=1)[0]
    df_da1 = df_da.drop(df_da.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 25]], axis=1)
    time.sleep(13)

    # ----------------------------------------Possession Formatting---------------------------------------
    df_po = pd.read_html(str(table_po), skiprows=1)[0]
    df_po1 = df_po.drop(df_po.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 32]], axis=1)
    time.sleep(13)

    # ----------------------------------------Misc Formatting---------------------------------------
    df_misc = pd.read_html(str(table_mi), skiprows=1)[0]
    df_misc1 = df_misc.drop(df_misc.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 25]], axis=1)
    time.sleep(13)

    result = pd.concat([df_sh1, df_ke1, df_pa1,df_pt1, df_GCA1, df_da1, df_po1, df_misc1], axis=1, join="inner")

    filename= f'chunk_{i // chunk_size +1}.csv' #name the csv based on which chunk it is
    result.to_csv(filename, index=False) # make the table a csv
    print('Formatted Table Built')
    time.sleep(60)
    print(time.strftime("%H,%M,%S"))



