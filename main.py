import pandas as pd
from Dictionary import Match_Logs_Type
from Dictionary import Premier_League_Teams
from Dictionary import La_Liga_Teams


First_Section= 'https://fbref.com/en/squads/'
#instead of VAR create a loop that iterates the last numebr of each year and then do it agian but +1
Current_Season_and_Filler= '/2023-2024/matchlogs/'
Twenty_Two_Season_and_Filler= '/2022-2023/matchlogs/'
Premier_League_Number= "c9"
LL_Number= "c12"
Match_Logs= '-Match-Logs-'
PL_League_Name= 'Premier-League'
LL_Name= 'La-Liga'

data = []

#Example url https://fbref.com/en/squads/361ca564/2023-2024/matchlogs/c9/shooting/Tottenham-Hotspur-Match-Logs-Premier-League
#            |      First_Section       |Team ID |   Year & Filler   |L#| M_L_T  | Team_Name      | Filler   | League Name  |

#2023-2024 PREMIER LEAGUE SEASON


for Team_Name,Team_ID in Premier_League_Teams.items(): #Calls to the dictionary Teams which includes Team names in URL Format and its ID number
  y= f'{First_Section}{Team_ID}'# https://fbref.com/en/squads/Team# n
  b= f'{Team_Name}'# Team Name

  for Match_Log_Type in Match_Logs_Type.values(): #Calls to the dictionary Match_Logs_Type which includes all the match log types
    a = f'{y}{Current_Season_and_Filler}{Premier_League_Number}/{Match_Log_Type}/{b}{Match_Logs}{PL_League_Name}'
    print(a)
    data.append(a)
#2022-2023 PREMIER LEAGUE SEASON
for Team_Name,Team_ID in Premier_League_Teams.items(): #Calls to the dictionary Teams which includes Team names in URL Format and its ID number
  y= f'{First_Section}{Team_ID}'# https://fbref.com/en/squads/Team# n
  b= f'{Team_Name}'# Team Name

  for Match_Log_Type in Match_Logs_Type.values(): #Calls to the dictionary Match_Logs_Type which includes all the match log types
    c = f'{y}{Twenty_Two_Season_and_Filler}{Premier_League_Number}/{Match_Log_Type}/{b}{Match_Logs}{PL_League_Name}'
    print(c)
    data.append(c)
#2023-2024 LA LIGA SEASON
for Team_Name,Team_ID in La_Liga_Teams.items(): #Calls to the dictionary Teams which includes Team names in URL Format and its ID number
  y= f'{First_Section}{Team_ID}'# https://fbref.com/en/squads/Team# n
  b= f'{Team_Name}'# Team Name

  for Match_Log_Type in Match_Logs_Type.values(): #Calls to the dictionary Match_Logs_Type which includes all the match log types
    d = f'{y}{Current_Season_and_Filler}{LL_Number}/{Match_Log_Type}/{b}{Match_Logs}{LL_Name}'
    print(d)
    data.append(d)

df = pd.DataFrame(data)
df.to_csv('Master_Links.csv', index=False)
