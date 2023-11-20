import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

df= pd.read_csv('Masterlink.csv') #Reads the CSV of mater links

chunk_size= 8 #There are 8 categories, therefore a chunk size of 8
total_rows= len(df) #Total amount of rows in the the master link

for i in range(0,total_rows, chunk_size):
    chunk_dataframe= df.iloc[i:i + chunk_size] #Iloc is used to pull rows from the dataframe, this is pulling 8 rows at a time i.e. the "Chunk size"
    Sh= chunk_dataframe.iloc[0]# This is creating a new dataframe of just the link for shooting so pulling a row of the chunk
    Shooting= Sh.to_string(header=False,index=False) #Dataframe store their datatypes as objects, in order to parse the link using the request library the link needs to be a string so its not converting the object to a string
    #print(Shooting)

    response_sh = requests.get(Shooting) # use request to pull up the webpage

    soup_sh = BeautifulSoup(response_sh.text, 'html.parser') #Use beautiful soup to parse the page into html

    table_sh = soup_sh.find('table') #Find the table in the page

    df_sh = pd.read_html(str(table_sh), skiprows=1)[0] #Use pandas to read the html, and pull out the table skipping the header row
    df_sh = df_sh.drop(df_sh.columns[[24]], axis=1) #drop certain columns so that it can be formated corectly
    df_sh1 = df_sh.drop(df_sh.index[-1]) #again formating the table


    filename= f'chunk_{i // chunk_size +1}.csv' #name the csv based on which chunk it is
    df_sh1.to_csv(filename, index=False) # make the table a csv

    print(f"Chunk {i // chunk_size +1}:\n",chunk_dataframe)
    print("\n"+ "="*40 + "\n")



